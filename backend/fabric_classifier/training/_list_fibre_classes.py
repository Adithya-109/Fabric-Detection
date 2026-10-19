import json
from pathlib import Path
root = Path('DATASETS/TextileNet-main/json')
classes = set()
for name in ['fibre_train.json','fibre_test.json']:
    items = json.loads((root/name).read_text(encoding='utf-8'))
    for _, cls, _ in items:
        classes.add(cls.lower())
for c in sorted(classes):
    print(c)
print('count', len(classes))
