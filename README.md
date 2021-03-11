# Thai Tokenizer
Fast and accurate Thai tokenization library using supervised [BPE](https://en.wikipedia.org/wiki/Byte_pair_encoding) designed for full-text search applications.



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
See [Training](TRAINING.md) for guidelines to train your own pairs.



## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.



## License
[MIT](https://choosealicense.com/licenses/mit/)
