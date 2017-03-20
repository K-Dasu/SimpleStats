from nltk import word_tokenize
from nltk import tag
from enum import Enum
import sys
import string

import trainer
sys.path.insert(0, '../Statistics')
from statsop import StatsOp
from cmdthesaurus import CmdThesaurus

class Open(Enum):
    NOT_OPEN_CMD = 0
    OPEN_FAIL = 1
    OPEN_SUCCESS = 2

class Synthesizer:

    def __init__(self):
        self.stats = StatsOp()
        self.thesaurus = CmdThesaurus()
        self.tagger = trainer.load_tagger('models/brown_all.pkl')

        self.labels = {}
        self.labels['verb'] = 'VB'
        self.labels['noun'] = 'NN'
        self.labels['nouns'] = 'NNS'

        self.specialNouns = []
        self.specialNouns.append('data')
        self.specialNouns.append('row')
        self.specialNouns.append('col')
        self.specialNouns.append('column')
        
        self.variables = [] # list of variables that we know
        self.commandStack = []

    def tokenize(self, cmd):
        return word_tokenize(cmd)

    def tag(self, tokens):
        return self.tagger.tag(tokens)

    def synonym_look_up(self,word):
        #check if word is in synonynm
        #return the appropriatly mapped word
        return word
    
    def print_requested (self, objs):
        word = ""
        number = -1
        isColumn = False
        isRow = False
        for item in objs:
            if word.lower() == "column":
                isColumn = True
            elif word.lower() == "row":
                isRow = True
        
            if item.isnumeric():
                number = int(item)
                
            if len(word) > 0:
                word = word + " " + str(item)
            else:
                word = str(item)
                
        if isColumn:
            corCol = self.stats.isAColumn(word, number)
            self.stats.printColumn(corCol)
        elif isRow:
            print("processing row...: number is: " + str(number))
            corRow = self.stats.isARow(word, number)
            self.stats.printRow(corRow)
    
    # If it's an open cmd
    def read_data_cmd(self, tokens): 
        if self.thesaurus.isOpenSynonym(tokens[0][0]): #handles case of reading in data
            # next argument must be filename, attempt to set up the data
            if self.stats.setData(tokens[-1][0]):
                print(tokens[-1][0] + ' has been successfully opened')
                return Open.OPEN_SUCCESS
            else:
                print('We couldn\'t find your file: ' + tokens[-1][0])
                return Open.OPEN_FAIL
        return Open.NOT_OPEN_CMD
    
     def print_data_cmd(self, tokens):
        print ("attempting to print..")
        command = self.build_command(tokens)
        print(self.commandStack)
        if tokens[0][0].lower() == 'show': # handles cases of printing or showing data
            [self.print_requested(n) for n in self.commandStack]
            self.commandStack = []
            
    def run_data_cmd(self, tokens):
        if tokens[0][0].lower() == 'command': # handles cases statistic commands on data
            print("printing out requested data")
            

    # parse a noun or none tag and see what it is
    def determine_var(self, nn):
        val = None

        # test if int
        try:
            val = int(nn)
            return val
        except ValueError:
            pass

        # test if float
        try:
            val = float(nn)
            return val
        except ValueError:
            pass

        # we now know val is a variable
        if val is None: # check if nn is even a column or row name
            return nn

    # checks to see if arg is a name inside list, row or col
    # returns True if it is
    def check_name_in_list(self, arg, li):
        if arg in li:
            return True
        else:
            return False
        
    def build_command(self, tokens):
        command = []
        previousNoun = False
        for pair in tokens:
            if(pair[1] == "VB"): #action to perform
                command.append(pair[0])
                self.commandStack.append(command)
                command = []
                
            if(pair[1] == "CD" and previousNoun): #cardinal number (or location) after a given noun
                command.append(pair[0])

            if(pair[1][0] == "N"): #noun
                command.append(pair[0])
                previousNoun = True
            else:
                previousNoun = False
            
            if(pair[1] == "CC"):
                self.commandStack.append(command)
                command = []
                
        self.commandStack.append(command)

    def synthesize(self, tagged, cmd):
        stats = self.stats
        labels = self.labels

        # Check if the command is an open command
        if self.read_data_cmd(tagged) != Open.NOT_OPEN_CMD:
            return # we attempted to open a file, so this command is finished

        # If we come across any nouns or nones, we need to check if it's been initialized
        # build_command call here, read is a special command

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
        

        # check if command 
        if tagged[0][1] == labels['verb']:
            print("Processing Verb")
            # Try to interpret this as a read initialization command
            if not stats.checkInitialized():
                self.read_data_cmd(tagged)
            else:
                print("Trying a non read command")
                command = self.synonym_look_up(tagged[0][0].lower())
                if command == "show":
                    self.print_data_cmd(tagged)
                pass # test printing column/row commands here?

        if tagged[0][1] == labels['noun'] or tagged[0][1] == labels['nouns']:

            print("Processing Noun")
            if not stats.checkInitialized():
                pass
            else:
                pass
        '''
