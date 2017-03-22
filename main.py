import sys
sys.path.insert(0, 'NLP')
import synthesis as syn

def main():

    print("Initializing synthesizer")
    # initialize synthesizer
    s = syn.Synthesizer()

    # Read commands
    while(1):
        print('Enter command:')
        cmd = input()
        tokens = s.tokenize(cmd)
        tagged = s.tag(tokens)

        print(tagged)
        if(s.thesaurus.isQuitSynonym(cmd)):
            break
        s.synthesize(tagged, cmd)


if __name__ == '__main__':
    main()