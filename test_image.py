import sys
import os
from PIL import Image

try:
    from backend.fabric_classifier.inference import FabricClassifier
except ImportError as e:
    print(f"Failed to import FabricClassifier: {e}")
    print("Ensure you are running this script from the root of the project.")
    sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_image.py <path_to_image>")
        print("Example: python test_image.py test_images/my_shirt.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    if not os.path.exists(image_path):
        print(f"Error: Image not found at '{image_path}'")
        sys.exit(1)

    weights_path = "backend/fabric_classifier/weights/fabric_clf_best.pt"
    if not os.path.exists(weights_path):
        print(f"Error: Weights file not found at '{weights_path}'")
        print("The model must be trained and weights saved before inference can run.")
        sys.exit(1)

    print("Initializing FabricClassifier...")
    try:
        clf = FabricClassifier(weights_path)
    except Exception as e:
        print(f"Failed to initialize FabricClassifier: {e}")
        sys.exit(1)

    print(f"Loading image: {image_path}")
    try:
        img = Image.open(image_path)
        img.load() # Ensure it's fully loaded and valid
    except Exception as e:
        print(f"Failed to load image: {e}")
        sys.exit(1)

    print("Running inference (extracting 7 patches and analyzing)...")
    try:
        results = clf.predict(img)
    except Exception as e:
        print(f"Inference failed: {e}")
        sys.exit(1)

    print("\n--- Predictions ---")
    if not results:
        print("No predictions returned.")
    else:
        for i, res in enumerate(results, 1):
            print(f"{i}. {res['name']}: {res['confidence']}%")
    print("-------------------")

if __name__ == "__main__":
    main()
