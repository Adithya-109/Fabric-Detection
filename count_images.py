import os
import sys
from PIL import Image

sys.path.append(os.getcwd())

try:
    from backend.fabric_classifier.classes import TEXTILENET_TO_TARGET
except ImportError as e:
    print(f'ImportError: {e}')
    sys.exit(1)

target_classes = ['Corduroy', 'Suede', 'Wool']
counts = {cls: 0 for cls in target_classes}
limit = 600

base_path = 'DATASETS/TextileNet-main'
subdirs = ['fabric', 'fibre']
splits = ['train', 'test']

for subdir in subdirs:
    for split in splits:
        path = os.path.join(base_path, subdir, split)
        if not os.path.exists(path):
            continue
        for class_name in os.listdir(path):
            target = TEXTILENET_TO_TARGET.get(class_name.lower())
            if target in target_classes:
                class_path = os.path.join(path, class_name)
                if not os.path.isdir(class_path):
                    continue
                for img_name in os.listdir(class_path):
                    if counts[target] >= limit:
                        break
                    img_path = os.path.join(class_path, img_name)
                    try:
                        with Image.open(img_path) as img:
                            img.verify()
                        counts[target] += 1
                    except Exception:
                        continue

print(f'Corduroy: {counts["Corduroy"]}, Suede: {counts["Suede"]}, Wool: {counts["Wool"]}')
