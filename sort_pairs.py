import sys
import json



pairs = []
with open(sys.argv[1], 'rt') as f:
    for line in (x.strip() for x in f):
        if line:
            pairs.append(tuple(json.loads(line)))

with open(sys.argv[1], 'wt') as f:
    for pair in sorted(set(pairs)):
        f.write(json.dumps(pair, ensure_ascii=False) + '\n')

print('Done.')
