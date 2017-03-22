import sys
sys.path.insert(0, 'NLP')
import synthesis as syn

def main():

    # initialize synthesizer
    d = False
    if(len(sys.argv) == 2 and sys.argv[1] == '-d'):
        d = True

    s = syn.Synthesizer(debug=d)

    # Read commands
    while(1):
        print('\nEnter command:')
        cmd = input()
        tokens = s.tokenize(cmd)
        tagged = s.tag(tokens)

        if d:
            print('Tagged tokens are: ' + str(tagged))
        if(s.thesaurus.isQuitSynonym(cmd)):
            print('Bye')
            break
        s.synthesize(tagged, cmd)


if __name__ == '__main__':
    main()
