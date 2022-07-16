from typing import Iterable


Pair = tuple[str, str]


def get_pairs(tokens:list[str]) -> set[Pair]:
    '''Get unique pairs from tokens.
    '''
    return set(zip(tokens[:-1], tokens[1:]))


class Index:
    def __init__(self, docs:Iterable[list[str]]):
        self.pair_to_count = {}
        self.pair_to_ix = {}
        for i, doc in enumerate(docs):
            for pair in set(get_pairs(doc)):
                self.incr_pair(pair)
                self.add_ix(pair, i)

    def incr_pair(self, pair:Pair):
        '''Increment pair counter.
        '''
        if pair not in self.pair_to_count:
            self.pair_to_count[pair] = 0
        self.pair_to_count[pair] += 1

    def decr_pair(self, pair:Pair):
        '''Decrement pair counter.
        '''
        #Skipped pairs cause KeyError if not handled.
        if pair in self.pair_to_count:
            self.pair_to_count[pair] -= 1
            if self.pair_to_count[pair] == 0:
                del self.pair_to_count[pair]

    def get_indices(self, pair:Pair):
        '''Get document indices where the pair is present.
        '''
        return tuple(self.pair_to_ix[pair])

    def add_ix(self, pair:Pair, ix:int):
        '''Add document index to a pair.
        '''
        if pair in self.pair_to_ix:
            self.pair_to_ix[pair].add(ix)
        else:
            self.pair_to_ix[pair] = set((ix,))

    def del_ix(self, pair:Pair, ix:int):
        '''Remove document index from the pair.
        '''
        #Skipped pairs cause KeyError if not handled.
        if pair in self.pair_to_ix:
            self.pair_to_ix[pair].remove(ix)
            if len(self.pair_to_ix[pair]) == 0:
                del self.pair_to_ix[pair]

    def get_top_pair(self) -> tuple[Pair, float]:
        '''Get pair with the most occurences.
        '''
        # TODO: Potential area for optimization.
        top_pair = max(self.pair_to_count, key=lambda x: self.pair_to_count[x])
        count = self.pair_to_count[top_pair]
        return top_pair, count / sum(self.pair_to_count.values())

    def __delitem__(self, pair:Pair):
        '''Completely remove the pair from the index in case of skipping.
        '''
        del self.pair_to_count[pair]
        del self.pair_to_ix[pair]

    def __contains__(self, pair:Pair):
        '''Check if the pair is in index.
        '''
        return pair in self.pair_to_ix or pair in self.pair_to_count
