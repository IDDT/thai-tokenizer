import os
import json


Pair = tuple[str, str]


class Merges:
    def __init__(self, filepath:str=''):
        self.merges = set()
        if filepath and os.path.isfile(filepath):
            with open(filepath, 'rt') as f:
                for line in f:
                    self.merges.add(tuple(json.loads(line.strip())))

    def __contains__(self, pair:Pair):
        return pair in self.merges

    def __len__(self):
        return len(self.merges)
