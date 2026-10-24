import base64
import binascii
import io
import os
import threading
import traceback

from flask import Flask, jsonify, render_template, request, send_from_directory
from PIL import Image, UnidentifiedImageError

from .fabric_classifier.classes import MATERIAL_CLASSES
from .fabric_classifier.profiles import FABRIC_PROFILES

MAX_UPLOAD_BYTES = 15 * 1024 * 1024  # 15 MB

# Sample images directory
SAMPLES_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "test_images", "samples")
)

AVAILABLE_SAMPLES = [
    {
        "id": "poly_cotton_check",
        "filename": "poly_cotton_check.jpeg",
        "title": "Check Weave Fabric",
        "subtitle": "Poly-cotton gingham check pattern",
        "badge": "Check Pattern"
    },
    {
        "id": "denim_sample",
        "filename": "denim_sample.jpg",
        "title": "Blue Twill Denim",
        "subtitle": "Diagonal twill indigo denim garment",
        "badge": "Denim Twill"
    },
    {
        "id": "silk_sample",
        "filename": "silk_sample.jpg",
        "title": "Emerald Silk Satin",
        "subtitle": "Glossy draped fluid silk sheen",
        "badge": "Silk / Satin"
    },
    {
        "id": "wool_knit_sample",
        "filename": "wool_knit_sample.jpg",
        "title": "Chunky Wool Knit",
        "subtitle": "Natural heathered looped knit yarn",
        "badge": "Wool Knit"
    }
]


class BadRequest(ValueError):
    """Client error that should be reported as HTTP 400."""


def _default_service_factory():
    # Imported here so that importing the app does not load PyTorch or the model.
    from .fabric_classifier.web_service import FabricWebService

    return FabricWebService()


def _decode_image(stream) -> Image.Image:
    try:
        image = Image.open(stream)
        image.load()  # force decode now, while the request stream is open
        return image
    except (UnidentifiedImageError, OSError, SyntaxError) as exc:
        raise BadRequest(f"Could not read the uploaded file as an image: {exc}") from exc


def _image_from_request() -> Image.Image:
    if "image" in request.files:
        file = request.files["image"]
        if not file.filename:
            raise BadRequest("Uploaded file has no filename.")
        return _decode_image(file.stream)

    payload = request.get_json(silent=True) or {}
    if "sample_id" in payload:
        sample_id = payload["sample_id"]
        match = next((s for s in AVAILABLE_SAMPLES if s["id"] == sample_id), None)
        if match is None:
            raise BadRequest(f"Unknown sample ID: {sample_id}")
        sample_path = os.path.join(SAMPLES_DIR, match["filename"])
        if not os.path.exists(sample_path):
            raise FileNotFoundError(f"Sample file not found: {match['filename']}")
        with open(sample_path, "rb") as f:
            return _decode_image(io.BytesIO(f.read()))

    if "image_base64" in payload:
        raw_b64 = str(payload["image_base64"])
        if "," in raw_b64:
            raw_b64 = raw_b64.split(",", 1)[1]
        try:
            img_bytes = base64.b64decode(raw_b64, validate=True)
        except (binascii.Error, ValueError) as exc:
            raise BadRequest("image_base64 is not valid base64.") from exc
        return _decode_image(io.BytesIO(img_bytes))

    raise BadRequest("No image provided. Upload a file, supply image_base64, or provide a sample_id.")


def create_app(service=None, service_factory=None) -> Flask:
    """Build the Flask app.

    The inference service is created on first use (``service_factory``), so importing
    or starting the app is fast and tests can inject a fake ``service``.
    """
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), "templates"),
        static_folder=os.path.join(os.path.dirname(__file__), "static"),
    )
    app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES

    factory = service_factory or _default_service_factory
    state = {"service": service}
    lock = threading.Lock()

    def get_service():
        if state["service"] is None:
            with lock:
                if state["service"] is None:
                    state["service"] = factory()
        return state["service"]

    app.extensions["fabric_service"] = get_service

    @app.errorhandler(413)
    def too_large(_err):
        limit_mb = MAX_UPLOAD_BYTES // (1024 * 1024)
        return jsonify({"error": f"Upload too large (limit {limit_mb} MB)."}), 413

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "online",
            "system": get_service().get_system_metrics(),
            "classes_count": len(MATERIAL_CLASSES),
            "service": "Fabric Classifier Web API",
        })

    @app.route("/api/classes", methods=["GET"])
    def get_classes():
        data = []
        for idx, name in enumerate(MATERIAL_CLASSES):
            profile = FABRIC_PROFILES.get(name, {})
            data.append({
                "index": idx,
                "name": name,
                "category": profile.get("category", "Textile Fabric"),
                "tagline": profile.get("tagline", ""),
                "properties": profile.get("properties", {}),
            })
        return jsonify({"classes": data})

    @app.route("/api/samples", methods=["GET"])
    def get_samples():
        return jsonify({"samples": AVAILABLE_SAMPLES})

    @app.route("/api/samples/<path:filename>", methods=["GET"])
    def serve_sample(filename):
        return send_from_directory(SAMPLES_DIR, filename)

    @app.route("/api/predict", methods=["POST"])
    def predict():
        try:
            pil_image = _image_from_request()
        except BadRequest as exc:
            return jsonify({"error": str(exc)}), 400
        except FileNotFoundError as exc:
            return jsonify({"error": str(exc)}), 404

        try:
            return jsonify(get_service().predict_image(pil_image))
        except Exception as exc:  # report, don't crash the server
            traceback.print_exc()
            return jsonify({"error": f"Inference failed: {exc}"}), 500

    return app


def warm_up(flask_app: Flask) -> None:
    """Load the model now instead of on the first request."""
    flask_app.extensions["fabric_service"]()


app = create_app()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    warm_up(app)
    print(f"Starting Fabric Classifier server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
