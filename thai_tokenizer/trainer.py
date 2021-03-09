import os
import json



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


class Index:
    def __init__(self, docs):
        self.pair_counts, self.pair_indices = {}, {}
        for i, doc in enumerate(docs):
            for pair in set(get_pairs(doc)):
                self.incr_pair(pair)
                self.add_ix(pair, i)

    def incr_pair(self, pair:tuple):
        '''Increment pair counter.
        '''
        if pair in self.pair_counts:
            self.pair_counts[pair] += 1
        else:
            self.pair_counts[pair] = 1

    def decr_pair(self, pair:tuple):
        '''Decrement pair counter.
        '''
        #Skipped pairs cause KeyError if not handled.
        if pair in self.pair_counts:
            self.pair_counts[pair] -= 1
            if self.pair_counts[pair] == 0:
                del self.pair_counts[pair]

    def get_indices(self, pair:tuple):
        '''Get document indices where the pair is present.
        '''
        return tuple(self.pair_indices[pair])

    def add_ix(self, pair:tuple, ix:int):
        '''Add document index to a pair.
        '''
        if pair in self.pair_indices:
            self.pair_indices[pair].add(ix)
        else:
            self.pair_indices[pair] = set((ix,))

    def del_ix(self, pair:tuple, ix:int):
        '''Remove document index from the pair.
        '''
        #Skipped pairs cause KeyError if not handled.
        if pair in self.pair_indices:
            self.pair_indices[pair].remove(ix)
            if len(self.pair_indices[pair]) == 0:
                del self.pair_indices[pair]

    def get_top_pair(self):
        '''Get pair with the most occurences.
        '''
        # TODO: Potential area for optimization.
        top_pair = max(self.pair_counts, key=self.pair_counts.get)
        count = self.pair_counts[top_pair]
        return top_pair, count / sum(self.pair_counts.values())

    def __delitem__(self, pair:tuple):
        '''Completely remove the pair from the index in case of skipping.
        '''
        del self.pair_counts[pair]
        del self.pair_indices[pair]

    def __contains__(self, pair:tuple):
        '''Check if the pair is in index.
        '''
        return pair in self.pair_indices or pair in self.pair_counts


def get_pairs(tokens:list) -> set:
    '''Get unique pairs from tokens.
    '''
    return set(zip(tokens[:-1], tokens[1:]))


def merge_pair(pair:tuple, tokens:list):
    '''Merge pair in tokens.
    Arguments:
        pair:Tuple[str]
            - 2 tokens forming a pair.
        tokens:List[str]
            - Variable length list of tokens.
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
