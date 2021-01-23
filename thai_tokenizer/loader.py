import re
import lzma
from .preprocessor import replace_thai_digits, whitespace_thai



def contains_thai(text:str) -> bool:
    return bool(re.search(r'[\u0E00-\u0E7F]', text))


def is_thai(text:str) -> bool:
    return bool(re.match(r'^[\u0E00-\u0E7F]*$', text))


def loader(fp):
    open = lzma.open if fp.endswith('.xz') else open
    with open(fp, 'rt') as f:
        for line in (line for line in f if contains_thai(line)):
            for doc in whitespace_thai(replace_thai_digits(line)).split():
                if is_thai(doc) and len(doc) > 1:
                    yield doc
