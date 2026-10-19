from pathlib import Path
from PIL import Image
root = Path('DATASETS/TextileNet-main/fibre')
paths = list((root / 'train' / 'suede').glob('*')) + list((root / 'test' / 'suede').glob('*'))
valid = 0
corrupt = 0
for p in paths:
    if not p.is_file():
        continue
    try:
        with Image.open(p) as img:
            img.verify()
        valid += 1
    except Exception:
        corrupt += 1
print(f'suede_total={valid+corrupt} valid={valid} corrupt={corrupt}')
