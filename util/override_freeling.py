
# Freeling tags to override and replace by other tags
TAGS = {'I': 'AQ0MS00', 'DP1MPP': 'AP0MP1P', 'AQVMP00':'AQ0MP00',
        'DP1MSP': 'AP0MS1P', 'DP1FPP': 'AP0FP1P', 'DP1FSP': 'AP0FS1P', 'AQVFS00': 'AQ0FS00'}

REPLACE_LEMMA_AND_TAG = {'ladra': {'lemma': 'ladrar', 'tag':'VMIP3S0'}, 'dió': {'lemma': 'dar', 'tag': 'VMIS3S0'},
                         'dios': {'lemma': 'dios', 'tag': 'NCMS000'},
                         'adiós': {'lemma': 'adiós', 'tag': 'NCMS000'},
                         'señor': {'lemma': 'señor', 'tag': 'NCMS000'},
                         }


DO_NOT_OVERRIDE = {'uf', 'je', 'ja', 'oh', 'todo_lo_contrario', 'ojalá'}

STEM_EQUALS_TAG = {'Z', 'W'}

