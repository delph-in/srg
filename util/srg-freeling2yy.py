################################################################################
#  Converting Freeling output into YY mode inputs for the SRG 
################################################################################

import sys, codecs
words = sys.stdin.readlines()
output = ""

# FREELING OUTPUT EXAMPLE (sentences are separated by a single new line):
# El el DA0MS0 1
# perro perro NCMS000 1
# duerme dormir VMIP3S0 0.989241
# . . Fp 1


sentid = 1
_num = 0       # lattice ID 
_from = 0      # lattice from
_from_c = 0    # character from
for line in words:
    if line.strip() != "":
        w = line.split()
        # print(w)
        surface = w[0]
        lemma = w[1]
        pos = w[2]
        conf = w[3]

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

    else:
        sentid += 1
        _num = 0       # lattice ID 
        _from = 0      # lattice from
        _from_c = 0    # character from
        output = output.strip() + "\n"
    
        
print(''.join(output.strip()))

