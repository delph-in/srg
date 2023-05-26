################################################################################
#  Converting Freeling output into YY mode inputs for the SRG
#  Author: Luis Morgado da Costa July 2022
#  Modified by: Olga Zamaraeva 2022-2023
#  Modified by: John Carroll April 2023
################################################################################

import sys
from override_freeling import TAGS, DO_NOT_OVERRIDE, STEM_EQUALS_TAG, REPLACE_LEMMA_AND_TAG, FUSE
import parse_sppp_dat

'''
In the old version of the grammar, some of the Freeling tags were overridden.
For compatibility, we will do the same for now.
i -> AQ0MS0 (interjection to a default adjective form; will then undergo an adjective-to-interjection rule...)
'''
def override_tag(selected, word, lemma, override_dicts):
    if lemma.isnumeric():
        return {'tag': 'Z', 'prob': -1}
    if selected['tag'] in TAGS and word not in DO_NOT_OVERRIDE and word not in REPLACE_LEMMA_AND_TAG:
        return {'tag': TAGS[selected['tag']], 'prob': -1 }
    if word in REPLACE_LEMMA_AND_TAG:
        return { 'tag': REPLACE_LEMMA_AND_TAG[word]['tag'], 'prob': -1 }
    if selected['tag'] in override_dicts['fuse']:
        return {'tag': override_dicts['fuse'][selected['tag']], 'prob': -1 }
    return selected
    #raise Exception("selected tag not in tag list")

def override_lemma(lemma, tag):
    if tag in STEM_EQUALS_TAG:
        return tag
    elif lemma in REPLACE_LEMMA_AND_TAG:
        return REPLACE_LEMMA_AND_TAG[lemma]['lemma']
    return lemma

def convert_sentences(sentences, override_dicts):
    yy_sentences = []
    for i, sent in enumerate(sentences):
        if i == 8:
            print("stop")
        output = ""
        _num = 0       # lattice ID
        _from = 0      # lattice from
        if not sent['tokens']:
            output = '(1,0,1, <0:{}>,1,"{}" "{}",0, "np00v00", "np00v00" 1.0)'.format(len(sent['sentence']),
                                                                                      sent['sentence'].replace('"','\\"'),
                                                                                      sent['sentence'].replace('"','\\"'))
        else:
            for j,tok in enumerate(sent['tokens']):
                surface = tok['form']
                tag_prob = {'tag': tok['selected-tag'], 'prob':tok['selected-prob']}
                pos_conf = override_tag(tag_prob, surface.lower(), tok['lemma'], override_dicts)
                pos = pos_conf['tag']
                conf = pos_conf['prob']
                lemma = override_lemma(tok['lemma'], pos)
                _num += 1
                output += '('
                output += str(_num)
                output += ', '
                output += str(_from)
                output += ', '
                _from += 1
                output += str(_from)
                output += ', <'
                output += str(int(tok['start'])) # - subtract)
                output += ':'
                output += str(int(tok['end'])) # - subtract)
                output += '>, 1, '
                output = output + '"' + lemma + '" ' if lemma != '"' else output + '"' + r'\"' + '" '
                output = output + '"' + surface +'", ' if surface != '"' else output + '"' + r'\"' + '", '
                output += '0, '
                output += '"' + pos +'", '                 # lrule
                output += '"' + pos +'" ' + "{:.8f}".format(float(conf))
                output += ') '
        #print(''.join(output.strip().lower()))
        yy_sentences.append(''.join(output.strip().lower()))
    return yy_sentences

if __name__ == "__main__":
    fuse, replace, no_disambiguate, output = parse_sppp_dat.parse_sppp('./freeling_api/srg-freeling.dat')
    override_dicts = {'fuse': fuse, 'replace': replace, 'no_disambiguate': no_disambiguate, 'output': output}
    # read FreeLing output from file or standard input; sentences are separated by one
    # or more blank lines
    if len(sys.argv) < 2 or sys.argv[1] == "-":
        f = sys.stdin
    else:
        f = open(sys.argv[1], 'r')
    sent = ""
    for ln in f:
        if ln.strip() == "": # inter-sentence blank line?
            if sent != "":
                print(convert_sentences([sent], override_dicts)[0])
                sent = ""
        else:
            sent += ln
    if sent != "":
        print(convert_sentences([sent], override_dicts)[0])
    if f is not sys.stdin:
        f.close()

    # sentences = convert_sentences_file(sys.argv[1])
    # for s in sentences:
    #     print(s)



