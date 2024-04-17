import sys
from tokenize_and_tag import Freeling_tok_tagger, PATH_TO_SPPP_DAT
from srg_freeling2yy import convert_sentences
import parse_sppp_dat
from override_freeling import ORDINALS as ordinals


if __name__ == "__main__":
    fuse, replace, no_disambiguate, output = parse_sppp_dat.parse_sppp(PATH_TO_SPPP_DAT)
    override_dicts = {'fuse': fuse, 'replace': replace, 'no_disambiguate': no_disambiguate, 'output': output,
                      'ordinals': ordinals}

    # read input from file or standard input, one sentence per line. Put each
    # sentence through FreeLing and convert the output to YY input format.
    ftok = Freeling_tok_tagger()
    if len(sys.argv) < 2 or sys.argv[1] == "-":
        f = sys.stdin
    else:
        f = open(sys.argv[1], 'r')
    for sent in f:
        if sent.strip() == "": # FreeLing doesn't cope well with empty input
            print("")
        else:
            freeling_s = ftok.tokenize_and_tag([sent], override_dicts)
            print(convert_sentences(freeling_s,override_dicts)[0])
    if f is not sys.stdin:
        f.close()
