################################################################################
#  Converting Freeling output into YY mode inputs for the SRG
#  Author: Luis Morgado da Costa July 2022
#  Modifies by: Olga Zamaraeva 2022-2023
################################################################################

import sys
from override_freeling import TAGS, DO_NOT_OVERRIDE, STEM_EQUALS_TAG, REPLACE_LEMMA_AND_TAG
#words = sys.stdin.readlines()

'''
In the old version of the grammar, some of the Freeling tags were overridden.
For compatibility, we will do the same for now.
i -> AQ0MS0 (interjection to a default adjective form; will then undergo an adjective-to-interjection rule...)
'''
def override_tag(selected, all, word):
    if selected in TAGS:
        if word not in DO_NOT_OVERRIDE:
            return {'tag': TAGS[selected], 'prob': -1 }
    elif word in REPLACE_LEMMA_AND_TAG:
        return { 'tag': REPLACE_LEMMA_AND_TAG[word]['tag'], 'prob': -1 }
    else:
        for t in all:
            if t['tag'] == selected:
                return t
        raise Exception("selected tag not in tag list")

def override_lemma(lemma, tag):
    if tag in STEM_EQUALS_TAG:
        return tag
    elif lemma in REPLACE_LEMMA_AND_TAG:
        return REPLACE_LEMMA_AND_TAG[lemma]['lemma']
    return lemma

def convert_sentences_file(sentence_file):
    if isinstance(sentence_file, str):
        with open(sentence_file, 'r') as f:
           corpus = f.read().split('\n\n')
    elif isinstance(sentence_file, list):
        corpus = sentence_file
    else:
        raise ValueError('The script was not given a list of sentences or a file with a list of sentences.')
    # FREELING OUTPUT EXAMPLE (sentences are separated by a single new line):
    # El el DA0MS0 1
    # perro perro NCMS000 1
    # duerme dormir VMIP3S0 0.989241
    # . . Fp 1
    yy_sentences = []
    for sent in corpus:
        output = ""
        sentid = 1
        _num = 0       # lattice ID
        _from = 0      # lattice from
        _from_c = 0    # character from
        for ln in sent.split('\n'):
            if ln.strip() != "":
                w = ln.split()
                # print(w)
                surface = w[0]
                conf = w[3]
                lemma = override_lemma(w[1], w[2])
                pos = override_tag(w[2], w[1], conf)
                _num += 1
                output += '('
                output += str(_num)
                output += ', '
                output += str(_from)
                output += ', '
                _from += 1
                output += str(_from)
                output += ', <'
                output += str(_from_c)
                output += ':'
                _from_c += len(surface)
                output += str(_from_c)
                output += '>, 1, '
                output += '"' + lemma +'" '
                output += '"' + surface +'", '
                output += '0, '
                output += '"' + pos +'", '                 # lrule
                output += '"' + pos +'" ' + conf
                output += ') '
                _from_c += 1   # assume a single space after the word
        #print(''.join(output.strip().lower()))
        yy_sentences.append(''.join(output.strip().lower()))
        # else:
        #     sentid += 1
        #     _num = 0       # lattice ID
        #     _from = 0      # lattice from
        #     _from_c = 0    # character from
        #     output = output.strip() + "\n"
    return yy_sentences

def convert_sentences(sentences):
    yy_sentences = []
    for i, sent in enumerate(sentences):
        output = ""
        _num = 0       # lattice ID
        _from = 0      # lattice from
        for j,tok in enumerate(sent['tokens']):
            surface = tok['form']
            best = override_tag(tok['selected-tag'],tok['all-tags'], tok['lemma'])
            pos = best['tag']
            conf = best['prob']
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
            output += '"' + lemma +'" '
            output += '"' + surface +'", '
            output += '0, '
            output += '"' + pos +'", '                 # lrule
            output += '"' + pos +'" ' + str(conf)
            output += ') '
        #print(''.join(output.strip().lower()))
        yy_sentences.append(''.join(output.strip().lower()))
    return yy_sentences

if __name__ == "__main__":
    sentences = convert_sentences_file(sys.argv[1])
    for s in sentences:
        print(s)



