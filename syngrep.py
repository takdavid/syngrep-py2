import glob, re, sys
from more_itertools import chunked
import nltk
from nltk import wordnet
from nltk.corpus.reader.wordnet import POS_LIST
from nltk.corpus import wordnet as wnc
wn = wordnet.wordnet
re_notword = re.compile(r'([^-\u2014\w]+)')
re_wholeword = re.compile(r'^[-\u2014\w]+$')
treebank_to_wordnet_pos = {'J': 'a', 'R': 'r', 'N': 'n', 'V': 'v'}
POS_CHUNKS = 100


def pivotize(pivot_str):
    if '.' in pivot_str:
        synsets = [wn.synset(pivot_str)]
        poss = [pivot_str.split('.')[1]]
    else:
        synsets = wn.synsets(pivot_str)
        poss = [ss.name().split('.')[1] for ss in synsets]
        if not synsets:
            global postagger
            postagger = False
    lemmata = []
    if synsets:
        for ss in synsets:
            lemmata.extend(ss.lemma_names())
            for hypo in ss.hyponyms():
                lemmata.extend(hypo.lemma_names())
    elif pivot_str:
        lemmata = [pivot_str]
    return (pivot_str, synsets, set(lemmata), set(poss))


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


def lemmatize(token, pos_list=POS_LIST):
    yielded = False
    for pos in pos_list:
        lemmas = wnc._morphy(token, pos)
        for lemma in lemmas:
            yield lemma
            yielded = True
    if not yielded:
        yield token


def words(corpus_glob):
    tokenlist = []
    global postagger
    for batch in chunked(filter(lambda x: is_word(x[0]), tokens(corpus_glob)), POS_CHUNKS):
        tokenlist = tokenlist[-POS_CHUNKS:] + [token for token, context in batch]
        poss = nltk.pos_tag(tokenlist) if postagger else []
        poses = [treebank_to_wordnet_pos.get(postuple[-1][0]) for postuple in poss[-POS_CHUNKS:]]
        for i, (token, context) in enumerate(batch):
            pos = poses[i] if postagger else None
            pos_list = [pos] if postagger and pos else POS_LIST
            word = (token, set(lemmatize(token, pos_list)), pos)
            yield word, context


def choose(word, pivot):
    if postagger and word[2] not in pivot[3]:
        return False
    if word[0] in pivot[2]:
        return True
    for lemma in word[1]:
        if lemma in pivot[2]:
            return True
    return False


def output(word, context):
    global last_output
    if last_output != context:
        print("%s:%d %s" % (context[0], context[1], context[2].strip()))
        last_output = context


_, pivot_str, corpus_glob = sys.argv
last_output = None
verbose = True
postagger = True
pivot = pivotize(pivot_str)
if verbose:
    sys.stdout.write(pivot[0] + ': ' + ((', '.join(ss.name() for ss in pivot[1])) or '?') + '; ' + ', '.join(sorted(pivot[2])) + '\n')
for word, context in words(corpus_glob):
    if choose(word, pivot):
        output(word, context)

