from nltk.corpus import wordnet as wn

#ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
class CmdThesaurus:

    def __init__(self):

        # verbs
        self.quitSynonyms = []
        self.openSynonyms = []
        self.showSynonyms = []
        self.calculateSynonyms = []
        # sums - total, sum, sigma
        # calculate, get
        # while, repeat

        # build quit synonyms
        self.quitSynonyms = buildSynList(self.quitSynonyms, "exit", wn.VERB)
        self.quitSynonyms = buildSynList(self.quitSynonyms, "quit", wn.VERB)
        self.quitSynonyms = list(set(self.quitSynonyms))

        #build read/open synonyms
        self.openSynonyms = buildSynList(self.openSynonyms, "read", wn.VERB)
        self.openSynonyms = buildSynList(self.openSynonyms, "open", wn.VERB)
        self.openSynonyms = list(set(self.openSynonyms))

        #build show/print synonyms
        self.showSynonyms = buildSynList(self.showSynonyms, "show", wn.VERB)
        self.showSynonyms = buildSynList(self.showSynonyms, "print", wn.VERB)
        self.showSynonyms = list(set(self.showSynonyms))

        #build show/print synonyms
        self.calculateSynonyms = buildSynList(self.calculateSynonyms, "get", wn.VERB)
        self.calculateSynonyms = buildSynList(self.calculateSynonyms, "calculate", wn.VERB)
        self.calculateSynonyms = list(set(self.calculateSynonyms))

        
    # returns true if word is a synonym of quit
    def isQuitSynonym(self, word):
        return (word in self.quitSynonyms)

    # returns true if word is a synonym of open
    def isOpenSynonym(self, word):
        return (word in self.openSynonyms)

    # returns true if word is a synonym of show
    def isOpenSynonym(self, word):
        return (word in self.showSynonyms)

    # returns true if word is a synonym of calculate
    def isCalculateSynonym(self, word):
        return (word in self.calculateSynonyms)

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
