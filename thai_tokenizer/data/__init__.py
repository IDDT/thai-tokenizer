import json
from importlib import resources



bpe_merges = []
for line in resources.open_text(__name__, 'bpe_merges.jsonl'):
    bpe_merges.append(tuple(json.loads(line)))
