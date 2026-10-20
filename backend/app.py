import os
import io
import base64
from flask import Flask, render_template, request, jsonify, send_from_directory
from PIL import Image

from .fabric_classifier.web_service import FabricWebService, FABRIC_PROFILES
from .fabric_classifier.classes import MATERIAL_CLASSES

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), "templates"),
    static_folder=os.path.join(os.path.dirname(__file__), "static")
)

# Initialize inference service once at startup
service = FabricWebService()

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


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    metrics = service.get_system_metrics()
    return jsonify({
        "status": "online",
        "system": metrics,
        "classes_count": len(MATERIAL_CLASSES),
        "service": "Fabric Classifier Web API"
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
            "properties": profile.get("properties", {})
        })
    return jsonify({"classes": data})


@app.route("/api/samples", methods=["GET"])
def get_samples():
    return jsonify({"samples": AVAILABLE_SAMPLES})


@app.route("/api/samples/<filename>", methods=["GET"])
def serve_sample(filename):
    return send_from_directory(SAMPLES_DIR, filename)


@app.route("/api/predict", methods=["POST"])
def predict():
    try:
        pil_image = None
        
        # 1. Check for multipart file upload
        if "image" in request.files:
            file = request.files["image"]
            if file.filename != "":
                pil_image = Image.open(file.stream)
                
        # 2. Check for sample selection
        elif request.is_json and "sample_id" in request.json:
            sample_id = request.json["sample_id"]
            match = next((s for s in AVAILABLE_SAMPLES if s["id"] == sample_id), None)
            if match:
                sample_path = os.path.join(SAMPLES_DIR, match["filename"])
                if os.path.exists(sample_path):
                    pil_image = Image.open(sample_path)
                else:
                    return jsonify({"error": f"Sample file not found: {match['filename']}"}), 404
            else:
                return jsonify({"error": f"Unknown sample ID: {sample_id}"}), 400
                
        # 3. Check for base64 encoded image
        elif request.is_json and "image_base64" in request.json:
            raw_b64 = request.json["image_base64"]
            if "," in raw_b64:
                raw_b64 = raw_b64.split(",", 1)[1]
            img_bytes = base64.b64decode(raw_b64)
            pil_image = Image.open(io.BytesIO(img_bytes))

        if pil_image is None:
            return jsonify({"error": "No image provided. Upload a file, supply image_base64, or provide a sample_id."}), 400

        # Run inference
        result = service.predict_image(pil_image)
        return jsonify(result)

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5050))
    print(f"Starting Fabric Classifier server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
