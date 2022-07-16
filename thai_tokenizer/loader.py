import re
import lzma
from typing import Iterator, Callable
from .preprocessor import replace_thai_digits, whitespace_thai
from .tcc import segment


def contains_thai(s:str) -> bool:
    return bool(re.search(r'[\u0E00-\u0E7F]', s))


def is_thai(s:str) -> bool:
    return bool(re.match(r'^[\u0E00-\u0E7F]*$', s))


def limiter(fn:Callable) -> Callable:
    def wrapper(arg, limit:int=0) -> Iterator:
        count = 0
        for item in fn(arg):
            count += 1
            if limit:
                if count % (limit // 20) == 0:
                    print(f'INFO: Loaded {count / limit * 100:.0f}%')
                if count > limit:
                    break
            yield item
    return wrapper


@limiter
def load_docs(filepath:str) -> Iterator[list[str]]:
    with lzma.open(filepath, 'rt') as f:
        for line in (x for x in f if contains_thai(x)):
            for split in whitespace_thai(replace_thai_digits(line)).split():
                if split and is_thai(split):
                    if len(doc := list(segment(split))) > 1:
                        yield doc
