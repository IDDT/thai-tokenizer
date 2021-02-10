import json
import argparse
from .tcc import segment
from .loader import loader
from .trainer import Merges, Index, merge



def main():
    parser = argparse.ArgumentParser(description='thai_tokenizer trainer')
    parser.add_argument('input', type=str,
        help='Mixed-thai newline separated documents.')
    parser.add_argument('-l', '--limit', type=int, default=0,
        help='Limit number of documents to load.')
    parser.add_argument('-n', '--n_merges', type=int, default=4000,
        help='Number of output merges.')
    parser.add_argument('-d', '--declined', type=str,
        default='temp/bpe_merges_declined.jsonl',
        help='Declined BPE merges.')
    parser.add_argument('-o', '--output', type=str,
        default='temp/bpe_merges.jsonl',
        help='BPE merges output for tokenization.')
    args = parser.parse_args()

    print('INFO: Loading documents...')
    docs = []
    for doc in loader(args.input):
        doc = list(segment(doc))
        if len(doc) > 1:
            docs.append(doc)
        if args.limit:
            if len(docs) % (args.limit // 20) == 0:
                print(f'INFO: Loaded {len(docs) / args.limit * 100:.0f}%')
            if len(docs) > args.limit:
                break

    print('INFO: Loading merges...')
    declined = Merges(args.declined)

    print('INFO: Calculating initial stats...')
    index = Index(docs)
    assert len(index.pair_counts) == len(index.pair_indices),\
        'This is likely a bug. Pair counts dont equal to number of indices.'

    print('INFO: Merging...')
    merges_out = merge(docs, index, declined, args.n_merges)

    #Save output.
    with open(args.output, 'wt') as f:
        for pair in merges_out:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')



if __name__ == '__main__':
    main()
