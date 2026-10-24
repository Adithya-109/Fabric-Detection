"""HTTP API tests for backend/app.py using a fake inference service.

No model or PyTorch is needed: the app factory accepts any object exposing
`predict_image(pil_image)` and `get_system_metrics()`.
"""
import base64
import io
import unittest

from tests import ROOT  # noqa: F401
from tests.helpers import image_bytes, noise_image
from backend.app import MAX_UPLOAD_BYTES, create_app


class FakeService:
    def __init__(self):
        self.calls = []

    def get_system_metrics(self):
        return {"device": "fake-cpu", "num_classes": 14}

    def predict_image(self, pil_image):
        self.calls.append(pil_image.size)
        top3 = [
            {"name": "Denim", "confidence": 70.0},
            {"name": "Cotton", "confidence": 20.0},
            {"name": "Linen", "confidence": 10.0},
        ]
        return {"prediction": top3[0], "top_3": top3}


class TestApi(unittest.TestCase):
    def setUp(self):
        self.service = FakeService()
        self.app = create_app(service=self.service)
        self.app.testing = True
        self.client = self.app.test_client()

    def test_health(self):
        r = self.client.get("/api/health")
        self.assertEqual(r.status_code, 200)
        body = r.get_json()
        self.assertEqual(body["status"], "online")
        self.assertEqual(body["classes_count"], 14)
        self.assertEqual(body["system"]["device"], "fake-cpu")

    def test_classes_lists_all_fourteen_in_contract_order(self):
        from backend.fabric_classifier.classes import MATERIAL_CLASSES

        body = self.client.get("/api/classes").get_json()
        self.assertEqual([c["name"] for c in body["classes"]], MATERIAL_CLASSES)
        self.assertEqual([c["index"] for c in body["classes"]], list(range(14)))

    def test_samples_listed_and_served(self):
        samples = self.client.get("/api/samples").get_json()["samples"]
        self.assertGreaterEqual(len(samples), 1)
        r = self.client.get(f"/api/samples/{samples[0]['filename']}")
        self.assertEqual(r.status_code, 200)
        r.close()

    def test_sample_path_traversal_blocked(self):
        r = self.client.get("/api/samples/..%2F..%2Fbackend%2Fapp.py")
        self.assertEqual(r.status_code, 404)

    def test_predict_with_uploaded_file(self):
        data = {"image": (image_bytes(noise_image((120, 80))), "cloth.png")}
        r = self.client.post("/api/predict", data=data, content_type="multipart/form-data")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json()["prediction"]["name"], "Denim")
        self.assertEqual(self.service.calls, [(120, 80)])

    def test_predict_with_base64_data_uri(self):
        raw = base64.b64encode(image_bytes(noise_image((64, 64)), "JPEG").read()).decode()
        r = self.client.post("/api/predict", json={"image_base64": f"data:image/jpeg;base64,{raw}"})
        self.assertEqual(r.status_code, 200)

    def test_predict_with_sample_id(self):
        r = self.client.post("/api/predict", json={"sample_id": "denim_sample"})
        self.assertEqual(r.status_code, 200)

    def test_missing_image_is_400(self):
        self.assertEqual(self.client.post("/api/predict", json={}).status_code, 400)
        self.assertEqual(self.client.post("/api/predict").status_code, 400)

    def test_empty_filename_is_400(self):
        data = {"image": (image_bytes(noise_image()), "")}
        r = self.client.post("/api/predict", data=data, content_type="multipart/form-data")
        self.assertEqual(r.status_code, 400)

    def test_non_image_upload_is_400_not_500(self):
        data = {"image": (io.BytesIO(b"definitely not an image"), "x.png")}
        r = self.client.post("/api/predict", data=data, content_type="multipart/form-data")
        self.assertEqual(r.status_code, 400)
        self.assertIn("error", r.get_json())
        self.assertEqual(self.service.calls, [])

    def test_bad_base64_is_400(self):
        r = self.client.post("/api/predict", json={"image_base64": "!!!not-base64!!!"})
        self.assertEqual(r.status_code, 400)

    def test_unknown_sample_is_400(self):
        self.assertEqual(self.client.post("/api/predict", json={"sample_id": "nope"}).status_code, 400)

    def test_oversized_upload_is_413_json(self):
        blob = b"0" * (MAX_UPLOAD_BYTES + 1024)
        data = {"image": (io.BytesIO(blob), "big.png")}
        r = self.client.post("/api/predict", data=data, content_type="multipart/form-data")
        self.assertEqual(r.status_code, 413)
        self.assertIn("error", r.get_json())

    def test_service_failure_is_500_json(self):
        def boom(_img):
            raise RuntimeError("model exploded")

        self.service.predict_image = boom
        data = {"image": (image_bytes(noise_image()), "cloth.png")}
        r = self.client.post("/api/predict", data=data, content_type="multipart/form-data")
        self.assertEqual(r.status_code, 500)
        self.assertIn("error", r.get_json())


class TestAppIsLazy(unittest.TestCase):
    def test_service_built_on_first_use_only(self):
        built = []

        def factory():
            built.append(1)
            return FakeService()

        app = create_app(service_factory=factory)
        client = app.test_client()
        self.assertEqual(built, [])
        client.get("/api/classes")
        self.assertEqual(built, [])  # static endpoint needs no model
        client.get("/api/health")
        client.get("/api/health")
        self.assertEqual(built, [1])


if __name__ == "__main__":
    unittest.main()
