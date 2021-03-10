import sys
import json

FILEPATH = sys.argv[1]



#Read pairs.
pairs = []
with open(FILEPATH, 'rt') as f:
    for line in (x.strip() for x in f):
        if line:
            pairs.append(tuple(json.loads(line)))

#Remove pairs with tokens resulting from mergine of a declined pair.
merged_pairs = set(''.join(pair) for pair in pairs)
pairs = [x for x in pairs if set(x).isdisjoint(merged_pairs)]

#Rewrite the file.
with open(FILEPATH, 'wt') as f:
    for pair in sorted(set(pairs)):
        f.write(json.dumps(pair, ensure_ascii=False) + '\n')

print('Done.')
