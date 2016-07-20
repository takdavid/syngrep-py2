import glob, re, sys
import nltk
from nltk import wordnet
from nltk.corpus.reader.wordnet import POS_LIST
from nltk.corpus import wordnet as wnc
wn = wordnet.wordnet
re_notword = re.compile(r'([^-\u2014\w]+)')
re_wholeword = re.compile(r'^[-\u2014\w]+$')


def pivotize(pivot_str):
    if '.' in pivot_str:
        synsets = [wn.synset(pivot_str)]
    else:
        synsets = wn.synsets(pivot_str)
    lemmata = []
    if synsets:
        for ss in synsets:
            lemmata.extend(ss.lemma_names())
            for hypo in ss.hyponyms():
                lemmata.extend(hypo.lemma_names())
    elif pivot_str:
        lemmata = [pivot_str]
    return (pivot_str, synsets, set(lemmata))


def tokenize(line):
    return re_notword.split(line)


def is_word(token):
    if re_wholeword.match(token):
        return True
    return False


def tokens(corpus_glob):
    for fn in glob.glob(corpus_glob):
        with open(fn, 'rb') as f:
            for i, _line in enumerate(f):
                line = _line.decode('utf-8')
                for token in tokenize(line):
                    yield token, (fn, i+1, line)


def lemmatize(token, context=None):
    yielded = False
    for pos in POS_LIST:
        lemmas = wnc._morphy(token, pos)
        for lemma in lemmas:
            yield lemma
            yielded = True
    if not yielded:
        yield token


def words(corpus_glob):
    for token, context in tokens(corpus_glob):
        if is_word(token):
            word = (token, set(lemmatize(token, context)), )
            yield word, context


def choose(word, pivot):
    if word[0] in pivot[2]:
        return True
    for lemma in word[1]:
        if lemma in pivot[2]:
            return True
    return False


def output(word, context):
    print("%s:%d %s" % (context[0], context[1], context[2].strip()))


_, pivot_str, corpus_glob = sys.argv
pivot = pivotize(pivot_str)
for word, context in words(corpus_glob):
    if choose(word, pivot):
        output(word, context)

