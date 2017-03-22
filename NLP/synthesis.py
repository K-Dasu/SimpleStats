from nltk import word_tokenize
from nltk import tag
from enum import Enum
import re
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

# special predecessor when parsing
class SpecialPred(Enum):
    COLUMN_SPEC = 0
    ROW_SPEC = 1 
    ORDINAL_NUMBER = 2
    APPLY_PRED = 3
    COMMA_PRED = 4
    AND_PRED = 5

class Synthesizer:

    def __init__(self):
        self.stats = StatsOp()
        self.thesaurus = CmdThesaurus()
        self.unitagger = trainer.load_tagger('models/brown_all_uni.pkl')
        #self.bitagger = trainer.load_tagger('models/brown_all_bi.pkl')
        #self.tritagger = trainer.load_tagger('models/brown_all_tri.pkl')

        # for matching if something is a cell
        self.cellReg = re.compile('[a-zA-Z]+[0-9]+')

        self.labels = {}
        self.labels['verb'] = 'VB'
        self.labels['noun'] = 'NN'
        self.labels['nouns'] = 'NNS'

        self.applyOps = ['by', 'to', 'from']
        
        self.variables = [] # list of variables that we know
        self.commandStack = []

    def tokenize(self, cmd):
        return word_tokenize(cmd)

    def tag(self, tokens):
        return self.unitagger.tag(tokens)

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
    def check_var_or_const(self, nn):
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

    # checks if the cell passed in refers to a cell, i.e. A1, bc23
    def check_cell(self, cell):
        return self.cellReg.fullmatch(cell) != None

    # build a command stack given list of tagged tokens
    '''
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
    '''

    # build a command given a list of tagged tokens
    # returns a pair representing a command
    def build_command(self, tokens):

        if tokens == []:
            return ('', [])

        pair = tokens[0]

        print(pair)

        # check column and rows for special terms
        # handle ordinal number
        if self.thesaurus.isColrow(pair[0]):

            # check if column/row followed by a number
            if len(tokens) >= 2:
                val = None
                try:
                    val = int(tokens[1][0])
                except ValueError:
                    pass

                if val is None:
                    return None
                else:
                    return ('evaluate', [pair[0], tokens[1][0]])

        # If it's a noun or none
        elif pair[1] is None or pair[1][0] == 'N' or pair[1] == 'CD':
            return ('evaluate', [pair[0]])
        # check if verb or special command type
        #elif pair[1] == 'CC' or pair[1] == ',':
        #    return (pair[0], [])
        #elif pair[0] in self.applyOps:
        #    return 
        elif pair[1][:2] == 'VB':
            return (pair[0], self.build_args(tokens[1:],[]))
        #else: # ignore this token
        #    return self.build_command(tokens[1:])

    # builds a list of arguments for a given command 
    def build_args(self, tokens, args):

        # out of tokens to construct arguments on
        if tokens == []:
            return args

        p = self.build_command(tokens)
        if p is not None:
            args.append(p)
            return self.build_args(tokens[1:], args)
        else:
            return self.build_args(tokens[1:], args)

    # where cmd is a pair ('cmd name', [list of args])
    def execute_command(self, cmd):

        if cmd[0] is None:
            print("Something went wrong...")
            return

        # calculate command
        if self.thesaurus.isCalculateSynonym(cmd[0]):
            return self.calculate_command(cmd[1])

        # show command
        elif self.thesaurus.isShowSynonym(cmd[0]):
            return self.show_command(cmd[1])

        # set command
        elif self.thesaurus.isSetSynonym(cmd[0]):
            pass



    # calculate only cares about the first argument, unless it's 
    # a special var like column 2
    def calculate_command(self, args):
        # something went wrong
        if len(args) == 0:
            print('something went wrong in a calculate command: no args')
            return

        arg = args[0]

        print('evaluating the pair: ' + str(arg))

        # if this is even a pair, we need to keep parsing
        if isinstance(arg, tuple):
            print('was tuple')
            return self.execute_command(arg)
        elif isinstance(arg, str):
            print('was string')
            # check if this is a column or row 'column __'
            if self.thesaurus.isColrow(arg):
                # if row/col number or name
                if self.stats.checkInitialized():
                    if len(args) > 1:
                        val = self.check_var_or_const(args[1])
                        if arg in self.thesaurus.columns:
                            #TODO get column
                            return self.stats.getColumn(val)
                        elif arg in self.thesaurus.rows:
                            return self.stats.getRow(val)
                        else:
                            return None
                    else: # argument list ended with col/row, haven't handled this case
                        return None
                else:
                    print('file hasn\'t been loaded so I don\'t have columns or rows yet')

            # check if this is a cell
            if self.check_cell(arg):
                print('was cell')
                if self.stats.checkInitialized():
                    return self.stats.getCellExcell(arg)
                else:
                    print('file hasn\'t been loaded so I don\'t know about ' + str(arg))

            # check if this is a variable name or constant
            val = self.check_var_or_const(arg)
            if val is None: # variable name -- must be a column
                if self.stats.checkInitialized():
                    columns = self.stats.getColumnNames()
                    if val in columns:
                        return self.stats.getColumn(val)
                    else:
                        print(val + ' is not a proper column name')
                        return None
                else:
                    print('file hasn\'t been loaded so I don\'t know about ' + str(val))
            else: # int or float
                return val


        else:
            print('something went wrong in a calculate command: invalid arg')

    def show_command(self, args):
        # something went wrong
        if len(args) == 0:
            print('something went wrong in a show command: no args')
            return

        arg = args[0]

        # if this is even a pair, we need to keep parsing
        if isinstance(arg, tuple):
            res = self.execute_command(arg)
            print(str(res))
            return res
        else:
            print(str(arg))
            return arg

    def set_command(self, args):
        # something went wrong
        if len(args) == 0:
            print('something went wrong in a set command: no args')
            return

        arg = args[0]

    def synthesize(self, tagged, cmd):
        stats = self.stats
        labels = self.labels

        # Check if the command is an open command
        if self.read_data_cmd(tagged) != Open.NOT_OPEN_CMD:
            return # we attempted to open a file, so this command is finished

        # If we come across any nouns or nones, we need to check if it's been initialized
        # build_command call here, read is a special command
        print("building command: ")
        c = self.build_command(tagged)
        print('c is ' + str(c))
        res = self.execute_command(c)
        print(res)
        return res


        # Call the command -- based on the command call a list of stat ops

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
