import json, os, pandas as pd
base = r'backend/fabric_classifier/training'
files = ['training_log.json', 'epoch_progress.jsonl', 'issues_log.json', '../../HANDOFF.md']
for f in files:
    p = os.path.join(base, f) if 'HANDOFF' not in f else f
    exists = os.path.exists(p)
    print(f'File: {p}, Exists: {exists}')
    if exists:
        with open(p, 'r') as file:
            content = file.read(500)
            print(f'Content preview:\n{content}\n' + '-'*20)
