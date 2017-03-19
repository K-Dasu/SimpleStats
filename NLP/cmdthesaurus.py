from nltk.corpus import wordnet as wn

#ADJ, ADJ_SAT, ADV, NOUN, VERB = 'a', 's', 'r', 'n', 'v'
class CmdThesaurus:

    def __init__(self):

        self.quitSynonyms = []
        self.openSynonyms = []
        synonyms = []

        # build quit synonyms
        synonyms = self.buildSynList(synonyms, "exit", wn.VERB)
        synonyms = list(set(synonyms))

        synonyms = self.buildSynList(synonyms, "quit", wn.VERB)
        synonyms = list(set(synonyms))

        self.quitSynonyms = synonyms

        #build read/open synonyms
        synonyms = []

        synonyms = self.buildSynList(synonyms, "read", wn.VERB)
        synonyms = list(set(synonyms))

        synonyms = self.buildSynList(synonyms, "open", wn.VERB)
        synonyms = list(set(synonyms))

        self.openSynonyms = synonyms


    # returns true if word is a synonym of quit
    def isQuitSynonym(self, word):
        return (word in self.quitSynonyms)

    # returns true if word is a synonym of quit
    def isOpenSynonym(self, word):
        return (word in self.openSynonyms)

    # adds synonyms of words to a list
    # li - the list to add to -- will return this
    # word - the word to find synonyms for
    # pos - the type of word it is, i.e. noun, verb, etc. as a char, see 
    # the wordnet pos list, see comment at top of class
    def buildSynList(self, li, word, pos):

        # filters out words based on pos
        for syn in [x for x in wn.synsets(word) if x.pos() == pos]:
            for l in syn.lemmas():
                li.append(l.name())
        return li
