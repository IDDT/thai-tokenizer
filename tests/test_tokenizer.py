import unittest
from thai_tokenizer import Tokenizer



class TestTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = Tokenizer([])

    def test_merge(self):
        tokens = ['a', 'b', 'c', 'd', 'e', 'f']
        tokens_out = (
            ['ab', 'c', 'd', 'e', 'f'],
            ['a', 'bc', 'd', 'e', 'f'],
            ['a', 'b', 'cd', 'e', 'f'],
            ['a', 'b', 'c', 'de', 'f'],
            ['a', 'b', 'c', 'd', 'ef']
        )
        for i in range(len(tokens) - 1):
            self.assertEqual(
                self.tokenizer._merge(tokens, pair_ix=i),
                tokens_out[i]
            )
