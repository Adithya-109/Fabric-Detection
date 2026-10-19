import os, sys
sys.path.insert(0, os.path.abspath('.'))
from collections import defaultdict
from backend.fabric_classifier.classes import MATERIAL_CLASSES, TEXTILENET_TO_TARGET
IMAGE_EXTENSIONS = ('.png','.jpg','.jpeg','.bmp','.webp')
source_dirs = ['DATASETS/TextileNet-main/fabric','DATASETS/TextileNet-main/fibre','DATASETS/TextileNet-main/None']
target_to_files = defaultdict(list)
for source_dir in source_dirs:
    if not os.path.isdir(source_dir):
        continue
    for split in ['train','test']:
        split_dir = os.path.join(source_dir, split)
        if not os.path.isdir(split_dir):
            continue
        for source_class in os.listdir(split_dir):
            class_dir = os.path.join(split_dir, source_class)
            if not os.path.isdir(class_dir):
                continue
            target = TEXTILENET_TO_TARGET.get(source_class.lower())
            if target not in MATERIAL_CLASSES:
                continue
            for f in os.listdir(class_dir):
                if f.lower().endswith(IMAGE_EXTENSIONS):
                    target_to_files[target].append(os.path.join(class_dir, f))
for c in MATERIAL_CLASSES:
    dedup = list(dict.fromkeys(target_to_files[c]))
    print(f'{c}\t{len(dedup)}')
