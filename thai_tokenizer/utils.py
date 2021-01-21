import re



def contains_thai(text:str) -> bool:
    return bool(re.search(r'[\u0E00-\u0E7F]', text))

def is_thai(text:str) -> bool:
    return bool(re.match(r'^[\u0E00-\u0E7F]*$', text))

def replace_thai_numbers(text:str) -> str:
    return text\
        .replace('๐', '0')\
        .replace('๑', '1')\
        .replace('๒', '2')\
        .replace('๓', '3')\
        .replace('๔', '4')\
        .replace('๕', '5')\
        .replace('๖', '6')\
        .replace('๗', '7')\
        .replace('๘', '8')\
        .replace('๙', '9')

def split_thai_nonthai(text:str) -> str:
    text = re.sub(f"(?<![\u0E00-\u0E7F])(?=[\u0E00-\u0E7F])|"
        f"(?<=[\u0E00-\u0E7F])(?![\u0E00-\u0E7F])", " ", text)
    return text.strip()
