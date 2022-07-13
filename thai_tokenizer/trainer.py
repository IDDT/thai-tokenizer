import json
from .index import Index
from .merges import Merges


Pair = tuple[str, str]


def get_pairs(tokens:list[str]) -> set[Pair]:
    '''Get unique pairs from tokens.
    '''
    return set(zip(tokens[:-1], tokens[1:]))


def merge_pair(pair:Pair, tokens:list[str]):
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


def merge(docs:list, index:Index, declined:Merges, n_merges:int):
    count = 0
    while count < n_merges:
        top_pair, proba = index.get_top_pair()
        #Feedback.
        top_pair_pretty = json.dumps(top_pair, ensure_ascii=False)
        print(f'#{count:04d} P:{proba * 100:.3f}%'
            f" {top_pair_pretty} -> \"{''.join(top_pair)}\"")
        #If pair in declined, remove it from the index.
        if top_pair in declined:
            print(f'Prevented merge for: {top_pair_pretty}')
            del index[top_pair]
            continue
        #If pair not in declined, merge pairs.
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
        #Send output.
        count += 1
        yield top_pair
