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
- `"ส่ง" + "ฟรี" | free + delivery -> freedelivery`
  - Separate since merging does not change the meaning of individual words.
- `"กาญจนา" + "ภิเษก" | kanjana + pisek = Kanajanapisek`
  - Merged because it is a name.
- `"แบต" + "เตอรี่" | Batt + tery = Battery`
  - Merged because it is anglicism.
- `"จักร" + "ยาน" | sewing machine + spacecraft (Bicycle)`  
  - Merged because new word arises from two seemingly unrelated tokens.
- `"ตำ" + "นาน" | pound + long (legend)`
  - Merged because of new meaning when merged that has nothing similar to initial tokens.
- `"ต่าง" + "หู" | different + ear (earrings)`
  - Merged because huge alter in meaning.
- `"กระ" + "เป๋า" | freckles + pouch`
  - Merged since leaving it separate would leave unwanted tokens. This merging is applicable to marketplace related tasks.
- `"เสื้อ" + "เชิ้ต" | shirt + shirt (button up shirt)`
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
