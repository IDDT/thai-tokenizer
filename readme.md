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
It might be desirable to train own pairs to capture the specifics of the dataset at hand. Figuring out which pairs should be merged can be highly subjective. As a general guideline here are some of the pairs that original author deemed as separate:
```
"ส่ง" + "ฟรี" | free + delivery -> freedelivery
"เจ้า" + "หญิง" | royal + woman = royalwoman (princess)
"งาน" + "แท้" | real + work = realwork (genuine)
"รอง" + "เท้า" | support + foot = supportfoot (shoe)
```
```bash
git clone thai_tokenizer
cd thai_tokenizer
python3 -m thai_tokenizer --help
```



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



## License
[MIT](https://choosealicense.com/licenses/mit/)
