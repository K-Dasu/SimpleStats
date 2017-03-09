import pandas as pd
from pickle import dump
from pickle import load
import nltk
import sys

# Trains and saves a tagger model to a file
# @filename name of file to save to
# @train_set the tagged set to train on
def train_and_save(filename, train_set):
    outfile = open(filename, 'wb')
    t = nltk.UnigramTagger(train_set)
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

# Uncomment to train
#brown_train = nltk.corpus.brown.tagged_sents(categories='news')
#train_and_save('brownnews.pkl',brown_train)

# Loads tagger, loop will take in sentence and return list of tagged tokens
t = load_tagger('models/brownnews.pkl')
while 1:
    print("Enter command:")
    cmd = input()
    tokens = nltk.word_tokenize(cmd)
    t.tag(tokens)
    tagged = t.tag(tokens)
    print(tagged)
