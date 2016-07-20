import glob, re, sys


re_notword = re.compile(r'([^-\u2014\w]+)')
re_wholeword = re.compile(r'^[-\u2014\w]+$')


def pivotize(pivot_str):
    return pivot_str


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


def lemmatize(token, context):
    return token


def words(corpus_glob):
    for token, context in tokens(corpus_glob):
        if is_word(token):
            word = lemmatize(token, context)
            yield word, context


def choose(word, pivot):
    return word == pivot


def output(word, context):
    print("%s:%d %s" % (context[0], context[1], context[2].strip()))


_, pivot_str, corpus_glob = sys.argv
pivot = pivotize(pivot_str)
for word, context in words(corpus_glob):
    if choose(word, pivot):
        output(word, context)

