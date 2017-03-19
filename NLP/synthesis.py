from nltk import word_tokenize
from nltk import tag
import sys
import string

import trainer
sys.path.insert(0, '../Statistics')
from statsop import StatsOp

class Synthesizer:

    def __init__(self):
        self.stats = StatsOp()
        self.tagger = trainer.load_tagger('models/brown_all.pkl')

        self.labels = {}
        self.labels['verb'] = 'VB'
        self.labels['noun'] = 'NN'

        self.specialNouns = []
        self.specialNouns.append('data')
        self.specialNouns.append('row')
        self.specialNouns.append('col')
        self.specialNouns.append('column')

    def tokenize(self, cmd):
        return word_tokenize(cmd)

    def tag(self, tokens):
        return self.tagger.tag(tokens)

    # attempt to initialize stats
    def read_data_cmd(self, tokens):
        if tokens[0][0].lower() is 'read':

            # next argument must be filename, attempt to set up the data
            if len(tokens) == 2:
                return self.stats.setData(tokens[0][1])


    # parse a noun or none tag and see what it is
    def parse_noun_or_none(self, nn):
        val = None

        # test if int
        try:
            val = int(nn)
        except ValueError:
            pass

        # test if int
        try:
            val = float(nn)
        except ValueError:
            pass

        # we now know val is a variable
        if val is None: # check if nn is even a column or row name
            pass

    # checks to see if arg is a name inside list, row or col
    # returns True if it is
    def check_name_in_list(self, arg, li):
        if arg in li:
            return True
        else:
            return False

    def synthesize(self, tagged, cmd):
        stats = self.stats
        labels = self.labels

        # check if we've already initialized
        '''
        if stats.checkInitialized():

            # Check if cmd is a row or column
            cols = stats.getColumnNames()
            rows = stats.getRowNames()

            if check_name_in_list(cmd, cols):
                print('name found in cols')
            elif check_name_in_list(cmd, rows):
                print('name found in rows')
        '''


        # check if command 
        if tagged[0][1] is labels['verb']:

            # Try to interpret this as a read initialization command
            if not stats.checkInitialized():
                read_data_cmd(tokens)
            else:
                pass # test printing column/row commands here?

        if tagged[0][1] is labels['noun']:

            if not stats.checkInitialized():
                pass
            else:
                pass


# initialize synthesizer
s = Synthesizer()

# Read commands
while(1):
    print('Enter command:')
    cmd = input()
    tokens = s.tokenize(cmd)
    tagged = s.tag(tokens)

    print(tagged)
    s.synthesize(tagged, cmd)