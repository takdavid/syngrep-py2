import unittest
from syngrep import tokenize, is_word

__all__ = ['TestSyngrep']


class TestSyngrep(unittest.TestCase):

    def test_tokenize(self):
        self.assertEqual(['It', 'was', 'a', 'bright', 'cold', 'day', 'in', 'April', 'and', 'the', 'clocks', 'were', 'striking', 'thirteen'],
                         filter(is_word, tokenize('It was a bright cold day in April, and the clocks were striking thirteen.')))