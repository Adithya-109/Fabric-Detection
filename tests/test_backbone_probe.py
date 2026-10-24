"""Tests for tools/backbone_probe.py (frozen-embedding comparison). NumPy/scikit-learn only:
real model extractors are replaced by fakes that return synthetic embeddings."""
import unittest

import numpy as np

from tests import ROOT  # noqa: F401
from tools import backbone_probe as bp

NAMES = ["Cotton", "Polyester", "Silk", "Denim"]


def blobs(n_per_class=40, dim=16, sep=3.0, seed=0, n_classes=4):
    rng = np.random.default_rng(seed)
    centres = rng.normal(size=(n_classes, dim)) * sep
    y = np.repeat(np.arange(n_classes), n_per_class)
    X = centres[y] + rng.normal(size=(len(y), dim))
    return X.astype(np.float32), y


class FakeExtractor:
    """Looks up a precomputed embedding by 'path' (an int index into X)."""

    def __init__(self, name, X, text_dim=None, text_table=None):
        self.name, self.X = name, X
        self._text_table = text_table
        if text_table is not None:
            self.embed_texts = self._embed_texts

    def embed_images(self, paths):
        return self.X[np.asarray(paths, dtype=int)]

    def _embed_texts(self, texts):
        return np.stack([self._text_table(t) for t in texts])


class TestHelpers(unittest.TestCase):
    def test_l2_normalize_unit_rows_and_zero_safe(self):
        X = np.array([[3.0, 4.0], [0.0, 0.0]])
        out = bp.l2_normalize(X)
        np.testing.assert_allclose(out[0], [0.6, 0.8])
        np.testing.assert_allclose(out[1], [0.0, 0.0])

    def test_build_prompts_covers_every_class_with_every_template(self):
        prompts = bp.build_prompts(NAMES, templates=["a photo of {} clothing", "{} fabric"])
        self.assertEqual(list(prompts), NAMES)
        for name in NAMES:
            self.assertEqual(len(prompts[name]), 2)
            self.assertTrue(all(name.lower() in p.lower() for p in prompts[name]))

    def test_default_prompts_cover_all_contract_classes(self):
        from backend.fabric_classifier.classes import MATERIAL_CLASSES

        prompts = bp.build_prompts(MATERIAL_CLASSES)
        self.assertEqual(list(prompts), MATERIAL_CLASSES)
        self.assertTrue(all(len(v) >= 2 for v in prompts.values()))

    def test_zero_shot_scores_pick_nearest_class_text(self):
        text = np.eye(4)  # one prompt-embedding per class
        img = np.array([[0.1, 0.9, 0, 0], [0, 0, 0.2, 0.8]])
        scores = bp.zero_shot_scores(img, [text[i:i + 1] for i in range(4)])
        self.assertEqual(scores.argmax(1).tolist(), [1, 3])

    def test_zero_shot_averages_multiple_prompts_per_class(self):
        # class 0 has two prompts pointing at +x and +y; the mean points between them
        texts = [np.array([[1.0, 0.0], [0.0, 1.0]]), np.array([[-1.0, -1.0]])]
        scores = bp.zero_shot_scores(np.array([[1.0, 1.0]]), texts)
        self.assertEqual(int(scores.argmax()), 0)


class TestToNumpy(unittest.TestCase):
    def test_plain_array_passes_through(self):
        np.testing.assert_array_equal(bp.to_numpy(np.ones((2, 3))), np.ones((2, 3)))

    def test_output_object_with_pooler_output_is_unwrapped(self):
        class Out:  # mimics transformers' BaseModelOutputWithPooling
            pooler_output = np.arange(6.0).reshape(2, 3)

        np.testing.assert_array_equal(bp.to_numpy(Out()), np.arange(6.0).reshape(2, 3))

    def test_object_with_numpy_method_is_converted(self):
        class T:
            def detach(self):
                return self

            def cpu(self):
                return self

            def numpy(self):
                return np.zeros(2)

        np.testing.assert_array_equal(bp.to_numpy(T()), np.zeros(2))

    def test_unknown_object_raises_clear_error(self):
        with self.assertRaises(TypeError):
            bp.to_numpy(object())


class TestHead(unittest.TestCase):
    def test_head_learns_separable_data_and_returns_scores_per_class(self):
        rng = np.random.default_rng(3)
        centres = rng.normal(size=(4, 16)) * 3
        mk = lambda n, s: (centres[np.repeat(np.arange(4), n)] + np.random.default_rng(s).normal(size=(4 * n, 16)),
                           np.repeat(np.arange(4), n))
        Xtr, ytr = mk(40, 10)
        Xte, yte = mk(20, 11)
        scores = bp.fit_predict_head(Xtr, ytr, Xte, n_classes=4, C=1.0)
        self.assertEqual(scores.shape, (80, 4))
        self.assertGreater((scores.argmax(1) == yte).mean(), 0.95)

    def test_head_handles_class_missing_from_training(self):
        X, y = blobs(n_classes=3)
        scores = bp.fit_predict_head(X, y, X[:5], n_classes=4, C=1.0)
        self.assertEqual(scores.shape, (5, 4))
        # the unseen class must never win
        self.assertNotIn(3, scores.argmax(1).tolist())

    def test_balanced_weighting_helps_minority_class(self):
        rng = np.random.default_rng(0)
        X = np.vstack([rng.normal(0, 1, (300, 2)), rng.normal(1.2, 1, (15, 2))])
        y = np.array([0] * 300 + [1] * 15)
        Xt = np.vstack([rng.normal(0, 1, (300, 2)), rng.normal(1.2, 1, (300, 2))])
        yt = np.array([0] * 300 + [1] * 300)
        rec = lambda s: ((s.argmax(1) == yt)[yt == 1]).mean()
        bal = bp.fit_predict_head(X, y, Xt, 2, C=1.0, balanced=True)
        raw = bp.fit_predict_head(X, y, Xt, 2, C=1.0, balanced=False)
        self.assertGreater(rec(bal), rec(raw))

    def test_choose_C_returns_value_from_grid(self):
        X, y = blobs(seed=4)
        c = bp.choose_C(X, y, n_classes=4, grid=(0.01, 1.0, 100.0), folds=3, seed=0)
        self.assertIn(c, (0.01, 1.0, 100.0))


class TestEvaluation(unittest.TestCase):
    def test_evaluate_scores_reports_balanced_accuracy_not_top1(self):
        y = np.array([0] * 8 + [1] * 2)
        scores = np.zeros((10, 4))
        scores[:, 0] = 1  # always predicts class 0
        res = bp.evaluate_scores(y, scores, NAMES)
        self.assertAlmostEqual(res["top1"], 0.8)
        self.assertAlmostEqual(res["balanced_accuracy"], 0.5)
        self.assertIn("macro_f1", res)
        self.assertIn("top3", res)

    def test_pairwise_auc_present_when_both_classes_exist(self):
        y = np.array([0, 0, 1, 1])
        scores = np.array([[2, 0, 0, 0], [1, 0, 0, 0], [0, 2, 0, 0], [0, 1, 0, 0]], dtype=float)
        res = bp.evaluate_scores(y, scores, NAMES)
        self.assertEqual(res["cotton_vs_polyester_auc"], 1.0)

    def test_pairwise_auc_none_when_class_absent(self):
        res = bp.evaluate_scores(np.array([0, 0]), np.zeros((2, 4)), NAMES)
        self.assertIsNone(res["cotton_vs_polyester_auc"])


class TestBootstrap(unittest.TestCase):
    def test_clearly_better_model_has_positive_interval(self):
        rng = np.random.default_rng(0)
        y = np.repeat(np.arange(4), 100)
        good = np.where(rng.random(400) < 0.8, y, rng.integers(0, 4, 400))
        bad = np.where(rng.random(400) < 0.3, y, rng.integers(0, 4, 400))
        res = bp.paired_bootstrap_diff(y, good, bad, n_boot=300, seed=0)
        self.assertGreater(res["diff"], 0.3)
        self.assertGreater(res["lo"], 0.0)
        self.assertLessEqual(res["lo"], res["diff"])
        self.assertGreaterEqual(res["hi"], res["diff"])

    def test_identical_models_interval_contains_zero(self):
        y = np.repeat(np.arange(4), 50)
        pred = np.roll(y, 3)
        res = bp.paired_bootstrap_diff(y, pred, pred, n_boot=100, seed=0)
        self.assertEqual(res["diff"], 0.0)
        self.assertEqual((res["lo"], res["hi"]), (0.0, 0.0))

    def test_deterministic_for_seed(self):
        y = np.repeat(np.arange(4), 30)
        a, b = np.roll(y, 1), np.roll(y, 2)
        r1 = bp.paired_bootstrap_diff(y, a, b, n_boot=50, seed=5)
        r2 = bp.paired_bootstrap_diff(y, a, b, n_boot=50, seed=5)
        self.assertEqual(r1, r2)


class TestRunProbe(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(0)
        self.centres = rng.normal(size=(4, 16)) * 3
        n_cal, n_eval = 40, 25
        self.y_cal = np.repeat(np.arange(4), n_cal)
        self.y_eval = np.repeat(np.arange(4), n_eval)
        draw = lambda y, s: (self.centres[y] + np.random.default_rng(s).normal(size=(len(y), 16))).astype(np.float32)
        # one shared table of embeddings: calib rows first, then eval rows
        self.X_good = np.vstack([draw(self.y_cal, 1), draw(self.y_eval, 2)])
        self.X_junk = np.random.default_rng(9).normal(size=self.X_good.shape).astype(np.float32)
        self.cal_paths = list(range(len(self.y_cal)))
        self.eval_paths = list(range(len(self.y_cal), len(self.y_cal) + len(self.y_eval)))

    def _run(self, extractors, baselines=None):
        return bp.run_probe(extractors, self.cal_paths, self.y_cal, self.eval_paths, self.y_eval, NAMES,
                            baselines=baselines, c_grid=(0.1, 1.0), seed=0, n_boot=100)

    def test_good_backbone_beats_junk_backbone(self):
        res = self._run([FakeExtractor("good", self.X_good), FakeExtractor("junk", self.X_junk)])
        self.assertGreater(res["models"]["good"]["linear"]["balanced_accuracy"], 0.9)
        self.assertLess(res["models"]["junk"]["linear"]["balanced_accuracy"], 0.5)
        self.assertEqual(res["ranking"][0], "good")

    def test_zero_shot_only_for_extractors_with_text_encoder(self):
        def table(text):  # embed the class name found in the prompt as a one-hot of the class centre
            for i, n in enumerate(NAMES):
                if n.lower() in text.lower():
                    return self.centres[i]
            return np.zeros(16)

        res = self._run([FakeExtractor("clip", self.X_good, text_table=table), FakeExtractor("dino", self.X_good)])
        self.assertIn("zero_shot", res["models"]["clip"])
        self.assertGreater(res["models"]["clip"]["zero_shot"]["balanced_accuracy"], 0.8)
        self.assertNotIn("zero_shot", res["models"]["dino"])

    def test_baseline_scores_are_evaluated_and_compared(self):
        rng = np.random.default_rng(1)
        baseline = rng.normal(size=(len(self.y_eval), 4))
        res = self._run([FakeExtractor("good", self.X_good)], baselines={"current_app_model": baseline})
        self.assertIn("current_app_model", res["models"])
        cmp_ = res["vs_baseline"]["good"]
        self.assertGreater(cmp_["diff"], 0.3)
        self.assertEqual(res["baseline_name"], "current_app_model")

    def test_scores_are_returned_for_saving(self):
        res = self._run([FakeExtractor("good", self.X_good)])
        self.assertEqual(res["scores"]["good/linear"].shape, (len(self.y_eval), 4))

    def test_chosen_C_recorded(self):
        res = self._run([FakeExtractor("good", self.X_good)])
        self.assertIn(res["models"]["good"]["linear"]["C"], (0.1, 1.0))

    def test_extractor_failure_is_recorded_not_fatal(self):
        class Boom(FakeExtractor):
            def embed_images(self, paths):
                raise RuntimeError("download failed")

        res = self._run([Boom("bad", self.X_good), FakeExtractor("good", self.X_good)])
        self.assertIn("download failed", res["errors"]["bad"])
        self.assertIn("good", res["models"])
        self.assertNotIn("bad", res["models"])


class TestReport(unittest.TestCase):
    def test_report_lists_models_and_baseline(self):
        rng = np.random.default_rng(0)
        y = np.repeat(np.arange(4), 10)
        X = (np.eye(4)[y] * 5 + rng.normal(size=(40, 4))).astype(np.float32)
        res = bp.run_probe([FakeExtractor("good", np.vstack([X, X]))], list(range(40)), y,
                           list(range(40, 80)), y, NAMES,
                           baselines={"current_app_model": rng.normal(size=(40, 4))},
                           c_grid=(1.0,), seed=0, n_boot=50)
        text = bp.render_report(res, NAMES, per_class_cap=10)
        self.assertIn("good", text)
        self.assertIn("current_app_model", text)
        self.assertIn("balanced", text.lower())

    def test_json_safe_strips_arrays(self):
        out = bp.json_safe({"scores": {"a": np.zeros((2, 2))}, "x": np.float32(1.5), "n": np.int64(3)})
        import json

        json.dumps(out)
        self.assertNotIn("scores", out)


if __name__ == "__main__":
    unittest.main()
