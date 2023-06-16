################################################################################
#  Converting Freeling output into YY mode inputs for the SRG
#  Author: Luis Morgado da Costa July 2022
#  Modified by: Olga Zamaraeva 2022-2023
#  Modified by: John Carroll April 2023
################################################################################

import sys
from override_freeling import TAGS, DO_NOT_OVERRIDE, STEM_EQUALS_TAG, REPLACE_LEMMA_AND_TAG
import parse_sppp_dat

'''
In the old version of the grammar, some of the Freeling tags were overridden.
For compatibility, we will do the same for now.
i -> AQ0MS0 (interjection to a default adjective form; will then undergo an adjective-to-interjection rule...)
'''
def override_tag(selected, word, lemma, override_dicts):
    if lemma.isnumeric():
        return {'tags': ['Z'], 'prob': -1}
    if selected['tag'] in TAGS and word not in DO_NOT_OVERRIDE and word not in REPLACE_LEMMA_AND_TAG:
        return {'tags': [TAGS[selected['tag']]], 'prob': -1 }
    if word in REPLACE_LEMMA_AND_TAG:
        return { 'tags': [REPLACE_LEMMA_AND_TAG[word]['tag']], 'prob': -1 }
    # Sometimes Freeling returns a sequence of two identical tags;
    # I am not sure what this means for the moment.
    # We will assume for now a single tag is sufficient.
    if '+' in selected['tag']:
        if selected['tag'] in override_dicts['fuse']:
            return {'tags': [override_dicts['fuse'][selected['tag']]], 'prob': -1}
        #print(selected['tag'])
        else:
            tags = selected['tag'].split('+')
            if len(tags) == 2:
                if tags[0][:-3] == tags[1]: # The first tag will have a trailing space followed by an extra quote mark, e.g. 'VMN0000 "'
                    return {'tags': [tags[0][:-3]], 'prob': -1 }
            else:
                print("More than two tags in Freeling output: {}".format(selected['tag']))
    if lemma in override_dicts['replace'] and len(override_dicts['replace'][lemma]['lemma']) == 1:
        return {'tags': override_dicts['replace'][lemma]['tag'], 'prob': -1 }
    return {'tags': [selected['tag']], 'prob': selected['prob']}
    #raise Exception("selected tag not in tag list")

def override_lemma(lemma, tag, override_dicts):
    if tag in STEM_EQUALS_TAG:
        return tag
    if lemma in override_dicts['replace']:
        # there may be more than one lemma-tag replacement pair; I have not yet figured out what to do with that
        return override_dicts['replace'][lemma]['lemma'][0]
    elif lemma in REPLACE_LEMMA_AND_TAG:
        return REPLACE_LEMMA_AND_TAG[lemma]['lemma']
    return lemma

def convert_sentences(sentences, override_dicts):
    yy_sentences = []
    for i, sent in enumerate(sentences):
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
                if len(pos_conf['tags']) > 1:
                    print("Warning: more than one tag for token: {}".format(tok['form']))
                pos = pos_conf['tags'][0]
                conf = pos_conf['prob']
                lemma = override_lemma(tok['lemma'], pos, override_dicts)
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



