import re
from .tcc import segment



class Tokenizer:
    def __init__(self, merge_pairs:list):
        self.pairs = {}
        for p, pair in enumerate(merge_pairs):
            self.pairs[tuple(pair)] = p

    @staticmethod
    def _merge(tokens:list, pair_ix:int) -> list:
        '''Merge list of tokens by pair index.
        '''
        a, b = pair_ix, pair_ix + 2
        return tokens[:a] + [''.join(tokens[a:b])] + tokens[b:]

    def split(self, text:str) -> list:
        '''Split Thai string into a list of tokens.
        Arguments:
            text:str
                - Contigious input of Thai characters.
        Returns:
            List[str]
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
                continue
            break
        return tokens

    def __call__(self, doc:str, sep:str=' ') -> str:
        '''Separate thai substrings in a mixed-language string.
        Arguments:
            doc:str
                - Document with optional Thai substrings.
            sep:str
                - Character to use a separator.
        '''
        for sub in re.findall('[\u0E00-\u0E7F]+', doc):
            doc = doc.replace(sub, sep.join(self.split(sub)))
        return doc
