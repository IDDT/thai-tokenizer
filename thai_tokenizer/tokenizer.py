import re
from typing import Iterable
from .tcc import segment
from .data import bpe_merges


Pair = tuple[str, str]


class Tokenizer:
    def __init__(self, pairs:Iterable[Pair]=bpe_merges):
        self.pairs = {}
        for p, pair in enumerate(pairs):
            assert len(pair) == 2,\
                'Pair should have exactly 2 tokens.'
            assert type(pair[0]) is str and type(pair[1]) is str,\
                'Both of the tokens in pair should be strings.'
            self.pairs[tuple(pair)] = p

    @staticmethod
    def _merge(tokens:list[str], pair_ix:int) -> list[str]:
        '''Merge list of tokens by pair index.
        '''
        a, b = pair_ix, pair_ix + 2
        return tokens[:a] + [''.join(tokens[a:b])] + tokens[b:]

    def split(self, text:str, debug:bool=False) -> list[str]:
        '''Split Thai string into a list of tokens.
        '''
        tokens = list(segment(text))
        while len(tokens) > 1:
            pairs = zip(tokens[:-1], tokens[1:])
            ix_min, pair_ix = None, None
            for i, ix in enumerate((self.pairs.get(pair) for pair in pairs)):
                if ix is not None and (ix_min is None or ix_min > ix):
                    ix_min, pair_ix = ix, i
            if pair_ix is not None:
                tokens = self._merge(tokens, pair_ix=pair_ix)
                if debug:
                    print(tokens)
                continue
            break
        return tokens

    def __call__(self, doc:str, sep:str=' ') -> str:
        '''Separate thai substrings in a mixed-language string.
        '''
        thai_substrings = re.findall('[\u0E00-\u0E7F]+', doc)
        for sub in sorted(thai_substrings, key=len, reverse=True):
            doc = doc.replace(sub, sep.join(self.split(sub)))
        return doc
