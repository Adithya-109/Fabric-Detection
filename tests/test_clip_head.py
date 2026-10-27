"""Tests for the embedding-based classifier (CLIP + linear head). A fake embedder stands in for CLIP,
so no model download or PyTorch is needed."""
import os
import shutil
import tempfile
import unittest

import numpy as np
from PIL import Image

from tests import ROOT  # noqa: F401
from tests.helpers import noise_image
from backend.fabric_classifier import clip_head as ch

NAMES = ["Cotton", "Polyester", "Silk", "Denim", "Knitted"]  # last class never seen in training


def make_data(n=30, dim=12, seed=0, n_seen=4):
    rng = np.random.default_rng(seed)
    centres = rng.normal(size=(n_seen, dim)) * 3
    y = np.repeat(np.arange(n_seen), n)
    return (centres[y] + rng.normal(size=(len(y), dim))).astype(np.float32), y, centres


class FakeEmbedder:
    def __init__(self, vec=None, dim=12):
        self.vec = np.ones(dim) if vec is None else np.asarray(vec)
        self.sizes = []

    def embed(self, pil_image):
        self.sizes.append(pil_image.size)
        return self.vec


class TestLinearHead(unittest.TestCase):
    def setUp(self):
        self.X, self.y, self.centres = make_data()
        self.head = ch.LinearHead.fit(self.X, self.y, NAMES, C=0.1)

    def test_probabilities_sum_to_one_and_cover_all_classes(self):
        p = self.head.probabilities(self.X[:7])
        self.assertEqual(p.shape, (7, len(NAMES)))
        np.testing.assert_allclose(p.sum(1), 1.0, atol=1e-9)

    def test_learns_separable_data(self):
        pred = self.head.probabilities(self.X).argmax(1)
        self.assertGreater((pred == self.y).mean(), 0.95)

    def test_unseen_class_never_predicted_and_has_zero_probability(self):
        p = self.head.probabilities(self.X)
        self.assertTrue((p[:, 4] < 1e-9).all())

    def test_matches_sklearn_pipeline(self):
        from sklearn.linear_model import LogisticRegression
        from sklearn.preprocessing import StandardScaler

        Xn = ch.l2_normalize(self.X)
        sc = StandardScaler().fit(Xn)
        clf = LogisticRegression(C=0.1, max_iter=3000, class_weight="balanced", random_state=0)
        clf.fit(sc.transform(Xn), self.y)
        expected = clf.predict_proba(sc.transform(Xn))
        np.testing.assert_allclose(self.head.probabilities(self.X)[:, :4], expected, atol=1e-6)

    def test_scale_invariance_of_embeddings(self):
        np.testing.assert_allclose(self.head.probabilities(self.X[:5]), self.head.probabilities(self.X[:5] * 7.5),
                                   atol=1e-9)

    def test_save_load_roundtrip(self):
        tmp = tempfile.mkdtemp()
        try:
            path = os.path.join(tmp, "head.npz")
            self.head.save(path)
            loaded = ch.LinearHead.load(path)
            self.assertEqual(loaded.class_names, NAMES)
            np.testing.assert_allclose(loaded.probabilities(self.X[:9]), self.head.probabilities(self.X[:9]))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def test_load_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            ch.LinearHead.load("/nonexistent/head.npz")

    def test_wrong_embedding_dim_raises(self):
        with self.assertRaises(ValueError):
            self.head.probabilities(np.ones((2, 5)))


class TestEmbeddingClassifier(unittest.TestCase):
    def setUp(self):
        self.X, self.y, self.centres = make_data()
        self.head = ch.LinearHead.fit(self.X, self.y, NAMES, C=0.1)
        self.embedder = FakeEmbedder(vec=self.centres[2])  # looks like class 2 (Silk)
        self.clf = ch.EmbeddingClassifier(self.embedder, self.head, max_side=512)
        self.image = noise_image((900, 700), seed=1)

    def test_predict_contract_three_sorted_known_classes(self):
        out = self.clf.predict(self.image)
        self.assertEqual(len(out), 3)
        self.assertEqual(out[0]["name"], "Silk")
        confs = [r["confidence"] for r in out]
        self.assertEqual(confs, sorted(confs, reverse=True))
        for r in out:
            self.assertEqual(set(r), {"name", "confidence"})
            self.assertIn(r["name"], NAMES)
            self.assertTrue(0 <= r["confidence"] <= 100)

    def test_predict_detailed_fields(self):
        d = self.clf.predict_detailed(self.image)
        self.assertEqual(set(d), {"top3", "probabilities", "patches", "timing"})
        self.assertAlmostEqual(float(np.sum(d["probabilities"])), 1.0, places=6)
        self.assertEqual(len(d["patches"]), 7)  # crops shown for inspection
        self.assertIn("patch_ms", d["timing"])
        self.assertIn("model_ms", d["timing"])
        self.assertEqual(d["top3"], self.clf.predict(self.image))

    def test_seven_inspection_patches_are_images_and_model_sees_whole_photo_once(self):
        self.embedder.sizes.clear()
        d = self.clf.predict_detailed(self.image)
        self.assertTrue(all(isinstance(p, Image.Image) for p in d["patches"]))
        self.assertEqual(len(self.embedder.sizes), 1)  # one embedding of the whole (resized) photo
        self.assertEqual(self.embedder.sizes[0], (512, 398))

    def test_patches_are_deterministic_for_same_image(self):
        a = self.clf.predict_detailed(self.image)["patches"]
        b = self.clf.predict_detailed(self.image)["patches"]
        for pa, pb in zip(a, b):
            np.testing.assert_array_equal(np.asarray(pa), np.asarray(pb))

    def test_patches_still_returned_for_plain_and_tiny_images(self):
        for img in (Image.new("RGB", (60, 40), (120, 90, 60)), Image.new("RGBA", (300, 300), (255, 255, 255, 255))):
            self.assertEqual(len(self.clf.predict_detailed(img)["patches"]), 7)

    def test_image_resized_before_embedding_and_rgb(self):
        self.clf.predict(self.image.convert("RGBA"))
        self.assertLessEqual(max(self.embedder.sizes[-1]), 512)

    def test_none_image_returns_contract(self):
        self.assertEqual(len(self.clf.predict(None)), 3)

    def test_exposes_attributes_the_web_service_reads(self):
        self.assertEqual(self.clf.class_names, NAMES)
        self.assertEqual(self.clf.temperature, 1.0)
        self.assertIsNone(self.clf.prior_correction)

    def test_deterministic(self):
        self.assertEqual(self.clf.predict(self.image), self.clf.predict(self.image))


class TextEmbedder(FakeEmbedder):
    """Fake CLIP: text embedding = class centre when the prompt names the class."""

    def __init__(self, centres, vec, names=NAMES):
        super().__init__(vec=vec)
        self.centres, self.names, self.text_calls = centres, names, 0

    def embed_texts(self, texts):
        self.text_calls += 1
        out = []
        for t in texts:
            hit = [i for i, n in enumerate(self.names) if n.lower() in t.lower()]
            out.append(self.centres_for(hit[0]) if hit else np.zeros(self.vec.shape[0]))
        return np.stack(out)

    def centres_for(self, i):
        return self.centres[i]


class TestZeroShotBlend(unittest.TestCase):
    def setUp(self):
        X, y, centres = make_data()
        rng = np.random.default_rng(5)
        self.centres = np.vstack([centres, rng.normal(size=(1, centres.shape[1])) * 3])  # + Knitted
        self.head = ch.LinearHead.fit(X, y, NAMES, C=0.1)

    def clf(self, blend, vec):
        emb = TextEmbedder(self.centres, vec)
        return ch.EmbeddingClassifier(emb, self.head, blend=blend), emb

    def probs(self, clf):
        return clf.predict_detailed(noise_image((300, 300)))["probabilities"]

    def test_zero_blend_is_head_only_and_never_loads_text(self):
        clf, emb = self.clf(0.0, self.centres[1])
        np.testing.assert_allclose(self.probs(clf), self.head.probabilities(self.centres[1])[0], atol=1e-9)
        self.assertEqual(emb.text_calls, 0)

    def test_full_blend_is_zero_shot_and_can_predict_class_unseen_by_head(self):
        clf, _ = self.clf(1.0, self.centres[4])  # looks like Knitted; the head never saw Knitted
        self.assertEqual(clf.predict(noise_image((300, 300)))[0]["name"], "Knitted")

    def test_half_blend_probabilities_valid_and_between_extremes_in_log_space(self):
        v = self.centres[2]
        p0, p1, ph = (self.probs(self.clf(w, v)[0]) for w in (0.0, 1.0, 0.5))
        self.assertAlmostEqual(float(ph.sum()), 1.0, places=6)
        mid = np.sqrt(p0 * p1)
        np.testing.assert_allclose(ph, mid / mid.sum(), atol=1e-6)  # geometric mean = log-space average

    def test_text_embeddings_computed_once(self):
        clf, emb = self.clf(0.5, self.centres[0])
        self.probs(clf)
        self.probs(clf)
        self.assertEqual(emb.text_calls, 1)

    def test_blend_needs_text_encoder_and_valid_range(self):
        with self.assertRaises(ValueError):
            ch.EmbeddingClassifier(FakeEmbedder(), self.head, blend=0.5)  # no embed_texts
        for bad in (-0.1, 1.5):
            with self.assertRaises(ValueError):
                ch.EmbeddingClassifier(TextEmbedder(self.centres, self.centres[0]), self.head, blend=bad)

    def test_blend_default_is_head_plus_zero_shot(self):
        self.assertEqual(ch.DEFAULT_BLEND, 0.5)

    def test_env_override_for_blend(self):
        self.assertEqual(ch.blend_from_env(None), ch.DEFAULT_BLEND)
        self.assertEqual(ch.blend_from_env("0"), 0.0)
        self.assertEqual(ch.blend_from_env("0.25"), 0.25)
        with self.assertRaises(ValueError):
            ch.blend_from_env("2")

    def test_prompts_and_zero_shot_helpers_available_without_tools_package(self):
        prompts = ch.build_prompts(NAMES, templates=["{} fabric"])
        self.assertEqual(prompts["Cotton"], ["cotton fabric"])


class TestModelChoice(unittest.TestCase):
    def test_auto_prefers_clip_head_when_file_exists(self):
        self.assertEqual(ch.choose_model_kind(None, head_exists=True), "clip_head")
        self.assertEqual(ch.choose_model_kind("", head_exists=True), "clip_head")

    def test_auto_falls_back_to_efficientnet_without_head(self):
        self.assertEqual(ch.choose_model_kind(None, head_exists=False), "efficientnet")

    def test_env_override_respected_case_insensitive(self):
        self.assertEqual(ch.choose_model_kind("EfficientNet", head_exists=True), "efficientnet")
        self.assertEqual(ch.choose_model_kind("clip_head", head_exists=False), "clip_head")

    def test_unknown_value_raises(self):
        with self.assertRaises(ValueError):
            ch.choose_model_kind("resnet", head_exists=True)


if __name__ == "__main__":
    unittest.main()


from tests.helpers import HAS_TORCH, TORCH_SKIP_REASON  # noqa: E402


@unittest.skipUnless(HAS_TORCH, TORCH_SKIP_REASON)
class TestWebServiceWithClipHead(unittest.TestCase):
    """The web service returns the full response schema when backed by the CLIP head."""

    def test_predict_image_schema_and_health(self):
        from backend.app import create_app
        from backend.fabric_classifier.web_service import FabricWebService

        X, y, centres = make_data()
        head = ch.LinearHead.fit(X, y, NAMES, C=0.1)
        clf = ch.EmbeddingClassifier(FakeEmbedder(vec=centres[3]), head)
        service = FabricWebService(classifier=clf)
        out = service.predict_image(noise_image((300, 200), seed=2))
        self.assertEqual(out["prediction"]["name"], "Denim")
        self.assertEqual(len(out["top_3"]), 3)
        self.assertEqual(len(out["all_classes"]), len(NAMES))
        self.assertEqual(len(out["patches"]), 7)
        self.assertIn("CLIP", out["metrics"]["model_backbone"])
        client = create_app(service=service).test_client()
        self.assertEqual(client.get("/api/health").get_json()["status"], "online")


class TestShippedHead(unittest.TestCase):
    def test_shipped_head_loads_and_matches_contract(self):
        from backend.fabric_classifier.classes import MATERIAL_CLASSES

        head = ch.LinearHead.load(ch.DEFAULT_HEAD_PATH)
        self.assertEqual(head.class_names, MATERIAL_CLASSES)
        self.assertEqual(head.mean.shape[0], 512)
        p = head.probabilities(np.random.default_rng(0).normal(size=(3, 512)))
        np.testing.assert_allclose(p.sum(1), 1.0, atol=1e-9)
