import json
import argparse
from .index import Index
from .loader import load_docs, limit_iterator
from .merges import Merges
from .trainer import merge



def main():
    parser = argparse.ArgumentParser(description='thai_tokenizer trainer')
    parser.add_argument('input', type=str,
        help='Mixed-thai newline separated documents.')
    parser.add_argument('-l', '--limit', type=int, default=0,
        help='Limit number of documents to load.')
    parser.add_argument('-n', '--n_merges', type=int, default=4000,
        help='Number of output merges.')
    parser.add_argument('-d', '--declined', type=str,
        help='Path to declined BPE merges file.')
    parser.add_argument('-o', '--output', type=str,
        default='temp/bpe_merges.jsonl',
        help='BPE merges output for tokenization.')
    args = parser.parse_args()

    print('INFO: Loading documents...')
    docs = list(limit_iterator(load_docs(args.input), args.limit))

    print('INFO: Loading merges...')
    declined = Merges(args.declined) if args.declined else Merges()

    print('INFO: Calculating initial stats...')
    index = Index(docs)
    assert len(index.pair_counts) == len(index.pair_indices),\
        'This is likely a bug. Pair counts dont equal to number of indices.'

    print('INFO: Merging & saving...')
    with open(args.output, 'wt') as f:
        for pair in merge(docs, index, declined, args.n_merges):
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')



if __name__ == '__main__':
    main()
