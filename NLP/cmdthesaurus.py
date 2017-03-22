from nltk.corpus import wordnet as wn

#ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
class CmdThesaurus:

    def __init__(self):

        # verbs
        self.quitSynonyms = []
        self.openSynonyms = []
        self.showSynonyms = []
        self.calculateSynonyms = []
        self.setSynonyms = []
        self.addSynonyms = []
        self.subSynonyms = []
        self.multSynonyms = []
        self.divSynonyms = []
        self.arithOps = []
        # sums - total, sum, sigma
        # calculate, get
        # while, repeat

        # nouns
        self.colrows = ['column', 'columns', 'col', 'cols', 'row', 'rows']
        self.columns = ['column', 'columns', 'col', 'cols']
        self.rows = ['row', 'rows']
        self.spreadsheetWords = ['all_data', 'spreadsheet']

        # statops
        self.statops = ['mode', 'median', 'mean', 'average', 
                        'deviation', 'min', 'minimum', 'max', 'maximum']

        # build quit synonyms
        self.quitSynonyms = buildSynList(self.quitSynonyms, "exit", wn.VERB)
        self.quitSynonyms = buildSynList(self.quitSynonyms, "quit", wn.VERB)
        self.quitSynonyms = list(set(self.quitSynonyms))

        #build read/open synonyms
        self.openSynonyms = buildSynList(self.openSynonyms, "read", wn.VERB)
        self.openSynonyms = buildSynList(self.openSynonyms, "open", wn.VERB)
        self.openSynonyms = list(set(self.openSynonyms))
        self.openSynonyms.remove('show')

        #build show/print synonyms
        self.showSynonyms = buildSynList(self.showSynonyms, "show", wn.VERB)
        self.showSynonyms = buildSynList(self.showSynonyms, "print", wn.VERB)
        self.showSynonyms = list(set(self.showSynonyms))

        #build show/print synonyms
        self.calculateSynonyms = buildSynList(self.calculateSynonyms, "get", wn.VERB)
        self.calculateSynonyms = buildSynList(self.calculateSynonyms, "calculate", wn.VERB)
        self.calculateSynonyms = buildSynList(self.calculateSynonyms, "see", wn.VERB)
        self.calculateSynonyms = buildSynList(self.calculateSynonyms, "evaluate", wn.VERB)
        self.calculateSynonyms.append("what")   # in statistical NLP, has the same purpose as calculate
        self.calculateSynonyms.append("eval")
        self.calculateSynonyms = list(set(self.calculateSynonyms))

        #build set synonyms -- need to consider set where there is no verb
        self.setSynonyms = buildSynList(self.setSynonyms, "set", wn.VERB)
        self.setSynonyms = buildSynList(self.setSynonyms, "change", wn.VERB)
        self.setSynonyms = buildSynList(self.setSynonyms, "modify", wn.VERB)
        self.setSynonyms = list(set(self.setSynonyms))

        # add synonyms
        self.addSynonyms = buildSynList(self.addSynonyms, 'add', wn.VERB)
        self.addSynonyms.append('increase')
        self.addSynonyms = list(set(self.addSynonyms))

        # subtract synonyms
        self.subSynonyms = buildSynList(self.subSynonyms, 'subtract', wn.VERB)
        self.subSynonyms.append('decrease')
        self.subSynonyms = list(set(self.subSynonyms))

        # multiply synonyms
        self.multSynonyms = buildSynList(self.multSynonyms, 'multiply', wn.VERB)
        self.multSynonyms = list(set(self.multSynonyms))

        # divide synonyms
        self.divSynonyms = buildSynList(self.divSynonyms, 'divide', wn.VERB)
        self.divSynonyms.append('divided')
        self.divSynonyms = list(set(self.divSynonyms))

        self.arithOps = self.addSynonyms + self.subSynonyms + self.multSynonyms + self.divSynonyms

    def isStatOp(self, word):
        return (word.lower() in self.statops)   

    def isSpreadsheet(self, word):
        return (word.lower() in self.spreadsheetWords)

    def isColrow(self, word):
        return (word.lower() in self.colrows)

    # returns true if word is a synonym of quit
    def isQuitSynonym(self, word):
        return (word.lower() in self.quitSynonyms)

    # returns true if word is a synonym of open
    def isOpenSynonym(self, word):
        return (word.lower() in self.openSynonyms)

    # returns true if word is a synonym of show
    def isShowSynonym(self, word):
        return (word.lower() in self.showSynonyms)

    # returns true if word is a synonym of calculate
    def isCalculateSynonym(self, word):
        return (word.lower() in self.calculateSynonyms)

    # returns true if word is a synonym of set
    def isSetSynonym(self, word):
        return (word.lower() in self.setSynonyms)

# adds synonyms of words to a list
# li - the list to add to -- will return this
# word - the word to find synonyms for
# pos - the type of word it is, i.e. noun, verb, etc. as a char, see 
# the wordnet pos list, see comment at top of class
def buildSynList(li, word, pos):

    # filters out words based on pos
    for syn in [x for x in wn.synsets(word) if x.pos() == pos]:
        for l in syn.lemmas():
            li.append(l.name())
    return li
