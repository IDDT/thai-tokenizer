import json
from typing import Iterator
from importlib import resources


Pair = tuple[str, str]


def _loader() -> Iterator[Pair]:
    for line in resources.open_text(__name__, 'bpe_merges.jsonl'):
        yield tuple(json.loads(line))


bpe_merges = tuple(_loader())
