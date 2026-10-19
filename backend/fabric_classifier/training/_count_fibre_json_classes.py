import json
from collections import Counter
from pathlib import Path
root = Path('DATASETS/TextileNet-main/json')
counts = Counter()
for name in ['fibre_train.json','fibre_test.json']:
    for _, cls, _ in json.loads((root/name).read_text(encoding='utf-8')):
        counts[cls.lower()] += 1
for cls, cnt in counts.most_common():
    print(f'{cls}\t{cnt}')
