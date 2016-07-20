import unittest

import nltk
from nltk.corpus.reader import Synset
from syngrep import tokenize, is_word, pivotize

__all__ = ['TestSyngrep']


class TestSyngrep(unittest.TestCase):

    def test_pivotize(self):
        pivot = pivotize('kid.v.02')
        self.assertEqual(pivot[0], 'kid.v.02')
        self.assertEqual(pivot[1], [nltk.wordnet.wordnet.synset('kid.v.02')])
        self.assertEqual(pivot[2], set([u'banter', u'chaff', u'josh', u'jolly', u'kid']))
        self.assertEqual(pivot[3], set(['v']))

    def test_tokenize(self):
        self.assertEqual(['It', 'was', 'a', 'bright', 'cold', 'day', 'in', 'April', 'and', 'the', 'clocks', 'were', 'striking', 'thirteen'],
                         filter(is_word, tokenize('It was a bright cold day in April, and the clocks were striking thirteen.')))