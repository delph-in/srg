
# Freeling tags to override and replace by other tags
TAGS = {'I': 'AQ0MS00', 'NP00O00':'NCFS000'}

# Sometimes Freeling gives a wrong tag in very simple cases, such as for the 3SG verb 'ladrar' it returns a noun tag
# with the probability 78%.
#LEMMA_TAG_PAIRS = {'NCFS000' : {'ladra': {'prob': 0.80, 'replace': 'VMIP3S0'}}}

REPLACE_LEMMA_AND_TAG = {'ladra': {'lemma': 'ladrar', 'tag':'VMIP3S0'}, 'dió': {'lemma': 'dar', 'tag': 'VMIS3S0'}}

DO_NOT_OVERRIDE = {'uf', 'je', 'ja'}

STEM_EQUALS_TAG = {'Z', 'W'}