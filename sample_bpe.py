import json
from thai_tokenizer import segment, ThaiTokenizer


with open('temp/bpe_merges.jsonl', 'rt') as f:
    tokenizer = ThaiTokenizer((json.loads(x)[0] for x in f))


tokenizer.tokenize('ศูนย์รวมล้อเดิมป้ายแดง')
