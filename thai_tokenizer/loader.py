import re
import lzma
from typing import Iterator
from .preprocessor import replace_thai_digits, whitespace_thai


def contains_thai(s:str) -> bool:
    return bool(re.search(r'[\u0E00-\u0E7F]', s))


def is_thai(s:str) -> bool:
    return bool(re.match(r'^[\u0E00-\u0E7F]*$', s))


def loader(fp) -> Iterator[str]:
    with lzma.open(fp, 'rt') as f:
        for line in (line for line in f if contains_thai(line)):
            for doc in whitespace_thai(replace_thai_digits(line)).split():
                if is_thai(doc) and len(doc) > 1:
                    yield doc
