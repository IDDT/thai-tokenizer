import re



def replace_thai_digits(text:str) -> str:
    '''Replace Thai digits for Arabic.
    '''
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

def whitespace_thai(text:str) -> str:
    '''Ensure Thai substrings are padded with whitespace.
    '''
    text = re.sub(f"(?<![\u0E00-\u0E7F])(?=[\u0E00-\u0E7F])|"
        f"(?<=[\u0E00-\u0E7F])(?![\u0E00-\u0E7F])", " ", text)
    return text.strip()
