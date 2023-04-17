import sys
from freeling.freeling_API.tokenize_and_tag import Freeling_tok_tagger
from srg_freeling2yy import convert_sentences




if __name__ == "__main__":
    # read input from file or standard input; sentences are separated by one
    # or more blank lines. Put the sentence through freeling and convert the
    # output to YY input format.
    ftok = Freeling_tok_tagger()
    if len(sys.argv) < 2 or sys.argv[1] == "-":
        f = sys.stdin
    else:
        f = open(sys.argv[1], 'r')
    sent = ""
    for ln in f:
        if ln.strip() == "": # inter-sentence blank line?
            if sent != "":
                freeling_s = ftok.tokenize_and_tag([sent])
                print(convert_sentences([freeling_s[0]]))
                sent = ""
        else:
            sent += ln
    if sent != "":
        freeling_s = ftok.tokenize_and_tag([sent])
        print(convert_sentences([freeling_s[0]]))
    if f is not sys.stdin:
        f.close()
