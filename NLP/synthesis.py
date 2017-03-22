from nltk import word_tokenize
from nltk import tag
from enum import Enum
import re
import sys
import string

import trainer
sys.path.insert(0, 'Statistics')
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
    
class Node:
    def __init__(self):
        self.children = []
        self.data = ""
    
    def getChildren(self):
        return self.children
    
    def addChild(self, child):
        self.children.append(child)
    
    def getData(self):
        return self.data
    
    def setData(self, value):
        self.data = value
    
    def printData(self):
        print(self.data)

class Synthesizer:

    def __init__(self):
        self.stats = StatsOp()
        self.thesaurus = CmdThesaurus()
        self.unitagger = trainer.load_tagger('NLP/models/brown_all_uni.pkl')
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

#----------------------------------------------------------------------->>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    def populateTree(self, node, taggedData):
        if len(taggedData) == 0: return node
        # print("Verb? " + taggedData[0][0])
        tag = taggedData[0][1]
        while tag is None or tag[0:2] != "VB":
            newNode = Node()
            if tag is None or tag[0] == 'N' or  tag[0:2] == "CD":
#                 print("Adding Child: " + taggedData[0][0] )
                newNode.setData(taggedData[0][0])
                node.addChild(newNode)
            taggedData.pop(0)
            if len(taggedData) == 0 : return node
            tag = taggedData[0][1]


        if tag is not None and tag[0:2] == "VB":
#             print("Adding Verb and its children: " + taggedData[0][0])
            newNode = Node()
            newNode.setData(taggedData[0][0])
            taggedData.pop(0)
            node.addChild(self.populateTree(newNode, taggedData))
            return node

    def printTree(self, node, i, mylist):
        if len(node.getChildren()) == 0:
            if len(mylist) > 0:
                return (node.getData() ,mylist)
            else:
                mylist.append(node.getData())
                return ("evaluate", mylist)
            
        childLen = len(node.getChildren())
        children = node.getChildren()
        index = 0
        while index < childLen:
            if len(children[index].getChildren()) > 0:
                mylist.append(self.printTree(children[index],i + 1,[]))
            else:
                #check if the sequence is column the # 
                evals = None
                if self.thesaurus.isColrow(children[index].getData()) and (index + 1 < childLen):
                    columnList = []
                    columnList.append(children[index].getData())
                    columnList.append(children[index + 1].getData())
                    evals = ("evaluate", columnList)
                    index = index + 1  
                else:    
                    evals = ("evaluate",children[index].getData())
                mylist.append(evals)
            index = index + 1    

        if len(mylist) > 0:
            return (node.getData() ,mylist)
        else:
            mylist.append(node.getData())
            return ("evaluate", mylist)

    def generateCommand(self, tagged):
        tree = Node()
        popTree = self.populateTree(tree,tagged)
        obj = None
        if len(popTree.getChildren()) > 1:
            popTree.setData("evaluate")
            obj = self.printTree(popTree, 0,[])
        else:
            actualTree = popTree.getChildren()[0]
            obj = self.printTree(actualTree, 0,[])
       
        return obj


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
            return self.set_command(cmd[1])

    # calculate only cares about the first argument, unless it's 
    # a special var like column 2
    def calculate_command(self, args):
        # something went wrong
        if len(args) == 0:
            print('something went wrong in a calculate command: no args')
            return

        if isinstance(args, list):
            arg = args[0]
        else:
            arg = args

        # if this is even a pair, we need to keep parsing
        if isinstance(arg, tuple):
            return self.execute_command(arg)
        elif isinstance(arg, str):
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
                if self.stats.checkInitialized():
                    return self.stats.getCellExcell(arg)
                else:
                    print('file hasn\'t been loaded so I don\'t know about ' + str(arg))


            if self.thesaurus.isSpreadsheet(arg):
                if self.stats.checkInitialized():
                    return self.stats.getData()
                else:
                    print('file hasn\'t been loaded so I don\'t have the data yet')

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
            print('Something went wrong in a calculate command: invalid arg')

    def show_command(self, args):
        # something went wrong
        if len(args) == 0:
            print('Something went wrong in a show command: no args')
            return

        if isinstance(args, list):
            arg = args[0]
        else:
            arg = args

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
        if len(args) < 2:
            print('Something went wrong in a set command: set needs at least 2 arguments')
            return

        des = args[0]   # the destination of what we're setting
        src = args[1]   # the source of what we're setting

        if isinstance(des, tuple) and isinstance(src,tuple):
            if des[0] == 'evaluate':

                # evaluate the src value
                res = self.execute_command(src)
                if res is None:
                    print('Something went wrong when trying to calculate the value to set')
                    return

                cell = des[1]
                if self.check_cell(cell):
                    if self.stats.checkInitialized():
                        self.stats.updateCellExcell(cell, res)
                        print(str(cell) + ' has been set to ' + str(res))
                        return res    
                    else:
                        print('file hasn\'t been loaded so I don\'t know about ' + str(des[1][0]))

            else:
                print("Something went wrong in trying to set a value to " + str(des[1]))
        else:
            print("Something went wrong in set command: invalid arg")

    def synthesize(self, tagged, cmd):
        stats = self.stats
        labels = self.labels

        # Check if the command is an open command
        if self.read_data_cmd(tagged) != Open.NOT_OPEN_CMD:
            return # we attempted to open a file, so this command is finished

        # If we come across any nouns or nones, we need to check if it's been initialized
        # build_command call here, read is a special command
        c = self.generateCommand(tagged)
        print('c is ' + str(c))
        res = self.execute_command(c)
        print(res)
        return res
