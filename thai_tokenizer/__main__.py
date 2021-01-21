import os
import lzma
import json
import argparse
from .tcc import segment
from .utils import contains_thai, is_thai
from .utils import replace_thai_numbers, split_thai_nonthai



class Merges:
    def __init__(self, filepath:str):
        self.merges, self.filepath = set(), filepath
        if os.path.isfile(self.filepath):
            with open(self.filepath, 'rt') as f:
                for line in f:
                    self.merges.add(tuple(json.loads(line.strip())))

    def __contains__(self, pair:tuple):
        return pair in self.merges

    def __len__(self):
        return len(self.merges)

    def add(self, pair:tuple):
        self.merges.add(pair)
        with open(self.filepath, 'at') as f:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')


class Index:
    def __init__(self, docs):
        self.pair_counts, self.pair_indices = {}, {}
        for i, doc in enumerate(docs):
            for pair in set(get_pairs(doc)):
                self.incr_pair(pair)
                self.add_ix(pair, i)

    def incr_pair(self, pair:tuple):
        if pair in self.pair_counts:
            self.pair_counts[pair] += 1
        else:
            self.pair_counts[pair] = 1

    def decr_pair(self, pair:tuple):
        #Skipped pairs cause KeyError if not handled.
        if pair in self.pair_counts:
            self.pair_counts[pair] -= 1
            if self.pair_counts[pair] == 0:
                del self.pair_counts[pair]

    def get_indices(self, pair:tuple):
        return tuple(self.pair_indices[pair])

    def add_ix(self, pair:tuple, ix:int):
        if pair in self.pair_indices:
            self.pair_indices[pair].add(ix)
        else:
            self.pair_indices[pair] = set((ix,))

    def del_ix(self, pair:tuple, ix:int):
        #Skipped pairs cause KeyError if not handled.
        if pair in self.pair_indices:
            self.pair_indices[pair].remove(ix)
            if len(self.pair_indices[pair]) == 0:
                del self.pair_indices[pair]

    def get_top_pair(self):
        top_pair = max(self.pair_counts, key=self.pair_counts.get)
        count = self.pair_counts[top_pair]
        return top_pair, count / sum(self.pair_counts.values()), count

    def __delitem__(self, pair:tuple):
        '''Completely remove the pair from the index in case of skipping.
        '''
        del self.pair_counts[pair]
        del self.pair_indices[pair]

    def __contains__(self, pair:tuple):
        '''Check if the pair is in index.
        '''
        return pair in self.pair_indices or pair in self.pair_counts


def loader(fp):
    open = lzma.open if fp.endswith('.xz') else open
    with open(fp, 'rt') as f:
        for line in (line for line in f if contains_thai(line)):
            for doc in split_thai_nonthai(replace_thai_numbers(line)).split():
                if is_thai(doc) and len(doc) > 1:
                    yield doc


def get_pairs(tokens:list) -> set:
    '''Get unique pairs from tokens.
    '''
    return set(zip(tokens[:-1], tokens[1:]))


def merge_pair(pair:tuple, tokens:list):
    '''Merge pair in tokens.
    '''
    pairs_before = get_pairs(tokens)
    out = tokens[:]
    while True:
        for i in range(1, len(out)):
            if pair[0] == out[i - 1] and pair[1] == out[i]:
                out = out[:i - 1] + [''.join(pair)] + out[i + 1:]
                break
        else:
            break
    pairs_after = get_pairs(out)
    pairs_incr = pairs_after - pairs_before
    pairs_decr = pairs_before - pairs_after
    return out, pairs_incr, pairs_decr


def merge(docs:list, index:Index, declined:Merges, accepted:Merges, n_merges:int) -> list:
    is_interactive = len(accepted) > 0
    out, max_merges = [], n_merges
    while len(out) < n_merges:
        top_pair, proba, count = index.get_top_pair()

        print(f"#{len(out):04d} P:{proba * 100:.3f}%"
            f" {' '.join(top_pair)} -> {''.join(top_pair)}")

        if is_interactive:
            if top_pair not in accepted and top_pair not in declined:
                if input('Merge? (default:y / n): ').strip() == 'n':
                    declined.add(top_pair)
                else:
                    accepted.add(top_pair)

        if top_pair in declined:
            print('INFO: Prevented merge for:', ' '.join(top_pair))
            del index[top_pair]
            continue
        out.append(top_pair)

        for i in index.get_indices(top_pair):
            docs[i], pairs_incr, pairs_decr = merge_pair(top_pair, docs[i])
            for pair in pairs_decr:
                index.decr_pair(pair)
                index.del_ix(pair, i)
            for pair in pairs_incr:
                index.incr_pair(pair)
                index.add_ix(pair, i)
        assert top_pair not in index, 'This is likely a bug. \
            The index should not contain the top_pair by now.'

    return out


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
    parser.add_argument('-a', '--accepted', type=str,
        default='temp/bpe_merges_accepted.jsonl',
        help='Accepted BPE merges, enters interactive mode if provided.')
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
            if len(docs) > args.limit:
                break
            elif len(docs) % (args.limit // 20) == 0:
                print(f'INFO: Loaded {int(len(docs) / args.limit * 100)}%')

    print('INFO: Loading merges...')
    declined = Merges(args.declined)
    accepted = Merges(args.accepted)
    is_interactive = True if args.accepted else False

    print('INFO: Calculating initial stats...')
    index = Index(docs)
    assert len(index.pair_counts) == len(index.pair_indices),\
        'This is likely a bug. Pair counts dont equal to number of indices.'

    print('INFO: Merging...')
    merges_out = merge(docs, index, declined, accepted, args.n_merges)

    #Save output.
    with open(args.output, 'wt') as f:
        for pair in merges_out:
            f.write(json.dumps(pair, ensure_ascii=False) + '\n')



if __name__ == '__main__':
    main()
