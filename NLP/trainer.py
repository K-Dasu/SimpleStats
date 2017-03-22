from pickle import dump
from pickle import load
import nltk
import sys


# Trains and saves a tagger model to a file
# @filename name of file to save to
# @train_set the tagged set to train on
# @num 1 - unigram, 2 - bigram, 3 - trigram
def train_and_save(filename, train_set, num):
    outfile = open(filename, 'wb')
    t = None
    if num == 1: #train a backoff
        t1 = nltk.UnigramTagger(train_set)
        t2 = nltk.BigramTagger(train_set, backoff=t1)
        model = {'everything': 'NN'}
        t = nltk.UnigramTagger(model = model, backoff = t2)
    elif num == 2:
        t = nltk.BigramTagger(train_set)
    elif num == 3:
        t = nltk.TrigramTagger(train_set)
    else:
        return
    dump(t, outfile, -1)
    outfile.close()

# Loads a tagger from file
# @filename
# @return tagger object
def load_tagger(filename):
    infile = open(filename, 'rb')
    t = load(infile)
    infile.close()
    return t

# Uncomment to train - Trains over ntlk brown corpus
#brown_train = nltk.corpus.brown.tagged_sents()
#train_and_save('models/brown_all_uni.pkl', brown_train, 1)
#train_and_save('models/brown_all_bi.pkl', brown_train, 2)
#train_and_save('models/brown_all_tri.pkl', brown_train, 3)

# Loads tagger, loop will take in sentence and return list of tagged tokens

def test_tagger():
    t = load_tagger('models/brown_all.pkl')
    while 1:
        print("Enter command:")
        cmd = input()
        tokens = nltk.word_tokenize(cmd)
        t.tag(tokens)
        tagged = t.tag(tokens)
        print(tagged)

