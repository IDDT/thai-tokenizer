# Thai Tokenizer
Fast and accurate Thai tokenization library using supervised BPE training designed for full-text search applications.



## Installation
```bash
pip3 install thai_tokenizer
```



## Usage
Default set of pairs is optimized for short Thai-English product descriptions.
```python
from thai_tokenizer import Tokenizer
tokenizer = Tokenizer()
tokenizer('iPad Mini 256GB เครื่องไทย') #> 'iPad Mini 256GB เครื่อง ไทย'
tokenizer.split('เครื่องไทย') #> ['เครื่อง', 'ไทย']
```



## Training
It might be desirable to train own pairs to capture the specifics of the dataset at hand. Figuring out which pairs should be merged can be highly subjective.
- `"อ" + "ง" | alphabets + alphabets"`
  - Separate because alphabets itself does not have meaning so those its merged result.
- `"ส่ง" + "ฟรี" | free + delivery -> freedelivery`
  - Separate since merging does not change the meaning of individual words.
- `"กาญจนา" + "ภิเษก" | kanjana + pisek = Kanajanapisek`
  - Given names should be merged.
- `"แบต" + "เตอรี่" | batt + tery = battery`
  - Merged because it is an anglicism.
- `"จักร" + "ยาน" | sewing machine + spacecraft = bicycle`  
  - Merged because the new token produces a token unrelated to the joined parts.
- `"ตำ" + "นาน" | pound + long = legend`
  - Same as above example.
- `"ต่าง" + "หู" | different + ear = earrings`
  - Merged because of significant alteration in the meaning.
- `"กระ" + "เป๋า" | freckles + pouch = handbag`
  - Merged because of significant alteration in meaning, additionally, the result produces a common word for everyday use.
- `"เสื้อ" + "เชิ้ต" | shirt + _modifier_word_ = button up shirt`
  - Separate because "shirt" should be available for full text matching. The modifier will be found through bi-gram matching.

```bash
git clone thai_tokenizer
cd thai_tokenizer
python3 -m thai_tokenizer --help
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



## License
[MIT](https://choosealicense.com/licenses/mit/)
