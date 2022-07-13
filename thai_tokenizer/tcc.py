import re
from typing import Iterator


TCC_REGEX = re.compile("|".join([
    "LEFT*+CONS+RIGHT*",
    "ๆ",
    "๚ะ๛|๚ะ|๚|๛",
    "ฯลฯ|ฯะ|ฯ",
    "๏|฿"
]).replace('+', '')\
    .replace("LEFT", r'[\u0E40-\u0E44]')\
    .replace("CONS", r'[\u0E01-\u0E2E]')\
    .replace("RIGHT", r'[\u0E30-\u0E3A\u0E45\u0E47-\u0E4E]')
)


def segment(s:str) -> Iterator[str]:
    i = 0
    while i < len(s):
        match_obj = TCC_REGEX.match(s[i:])
        end = match_obj.span()[1] if match_obj is not None else 1
        thai_tcc = s[i:i + end]
        i += end
        yield thai_tcc
