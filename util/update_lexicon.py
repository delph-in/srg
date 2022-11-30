import sys
import copy
from delphin import tdl as pydelphin_tdl

"""
This script helps to modify the grammar so that all entries in the lexicon are native lexical entries, as in, they
inherit from a supertype which inherits from native_le.

This is not a fully working script in the sense that it won't give you a fully working new version of letypes.tdl and
lexicon.tdl; you will need to (a) only copy over the updated portion of letypes starting from Leaf types; (b) change 
a couple more things manually until the grammar compiles.
"""

def update_lexicon(filepath_lex, filepath_letypes):
    le_to_update = set()
    for event, obj, lineno in pydelphin_tdl.iterparse(filepath_lex):
        if event == 'TypeDefinition':
            #print(pydelphin_tdl.format(obj))
            st = obj.supertypes[0]
            le_to_update.add(str(st))

    updated_letypes = []
    for event, obj, lineno in pydelphin_tdl.iterparse(filepath_letypes):
        if event == 'TypeDefinition':
            #print(pydelphin_tdl.format(obj))
            if obj.identifier in le_to_update:
                print(obj.identifier)
                new_id = add_word_to_typename(obj.identifier, '_native', '_le')
                ds = '' if not obj.docstring else obj.docstring
                conj = copy.deepcopy(obj.conjunction)
                new_type = pydelphin_tdl.TypeDefinition(new_id, conj, ds +
                                                        'This is a native lexical entry type, '
                                                        'for words that are in the lexicon.')
                new_type.conjunction.add(pydelphin_tdl.TypeIdentifier('native_le'))
                updated_letypes.append((event, new_type, lineno))
            updated_letypes.append((event, obj, lineno))
        else:
            updated_letypes.append((event, obj, lineno))
    save_tdl_objects(updated_letypes, 'updated_letypes.tdl')

    updated_lexical_entries = []
    for event, obj, lineno in pydelphin_tdl.iterparse(filepath_lex):
        if event == 'TypeDefinition':
            terms = [add_word_to_typename(obj.supertypes[0], '_native', '_le')]
            terms.extend(obj.conjunction.terms[1:])
            conj = pydelphin_tdl.Conjunction(terms)
            new_type = pydelphin_tdl.TypeDefinition(obj.identifier, conj, obj.docstring)
            updated_lexical_entries.append((event, new_type, lineno))
        else:
            updated_lexical_entries.append((event, obj, lineno))

    save_tdl_objects(updated_lexical_entries, 'updated_lexicon.tdl')


def save_tdl_objects(tdl_objects, filename):
    with open(filename, 'w') as f:
        for event, obj, lineno in tdl_objects:
            if event == 'LineComment':
                if not obj.startswith(';'):
                    f.write('; ' + obj + '\n')
                else:
                    f.write(obj + '\n')
            elif event == 'BlockComment':
                f.write('#|' + obj + '|#\n\n')
            else:
                f.write(pydelphin_tdl.format(obj) + '\n\n')


def add_word_to_typename(name, word, suffix):
    first_part = name[:len(name)-len(suffix)]
    return pydelphin_tdl.TypeIdentifier(first_part + word + suffix)

def create_generic_entries(tags, supertype, pred):
    entries = []
    for tag in tags:
        t = tag.strip()
        id = pydelphin_tdl.TypeIdentifier(t + '_ge')
        super_id = pydelphin_tdl.TypeIdentifier(supertype)
        v = [pydelphin_tdl.String(supertype)]
        token_id = pydelphin_tdl.TypeIdentifier('generic_token_list')
        pos_list = pydelphin_tdl.ConsList(values=[pydelphin_tdl.String(t)], end=pydelphin_tdl.EMPTY_LIST_TYPE)
        pos_avm = pydelphin_tdl.AVM([('+POS.+TAGS', pos_list)])
        tok_list = pydelphin_tdl.ConsList(values = [pos_avm], end=pydelphin_tdl.EMPTY_LIST_TYPE)
        token_conj = pydelphin_tdl.Conjunction([token_id, tok_list])
        term = pydelphin_tdl.AVM([('STEM', pydelphin_tdl.ConsList(values=v,end=pydelphin_tdl.EMPTY_LIST_TYPE)),
                                  ('TOKENS.+LIST', token_conj),
                                  ('SYNSEM.LKEYS.KEYREL.PRED', pydelphin_tdl.String('_generic_' + pred + '_rel'))])

        ds = 'Generic lexical entry that will be triggered by tag {}.'.format(t)
        terms = [super_id, term]
        conj = pydelphin_tdl.Conjunction(terms)
        new_type = pydelphin_tdl.TypeDefinition(id, conj, ds)
        entries.append(new_type)
    with open(pred + '_entries.tdl', 'w') as f:
        for e in entries:
            f.write(pydelphin_tdl.format(e) + '\n\n')

#update_lexicon(sys.argv[1],sys.argv[2])
adverbial_tags = ['rg', 'rn', 'nc00000']
v_tags = "vmip1s0, vmip2s0, vmip3s0, vmib1p0, vmip1p0, vmip2p0, vmii4s0, vmii2s0, vmii3s0, vmii1p0, vmii2p0, vmii3p0, vmis1s0, vmis2s0, vmis3s0, vmis1p0, vmis2p0, vmis3p0, vmif1s0, vmif2s0, vmif3s0, vmif1p0, vmif2p0, vmif3p0, vmic4s0, vmic1s0, vmic2s0, vmic3s0, vmic1p0, vmic2p0, vmic3p0, vmsp4s0, vmsp1s0, vmsp2s0, vmsp3s0, vmsp1p0, vmsp2p0, vmsp3p0, vmsi4s0, vmsi1s0, vmsi2s0, vmsi3s0, vmsi1p0, vmsi2p0, vmsi3p0, vmsf4s0, vmsf1s0, vmsf2s0, vmsf3s0, vmsf1p0, vmsf2p0, vmsf3p0, vmm02s0, vmm03s0, vmm01p0, vmm02p0, vmm03p0, vmn0000, vmg0000, vmp0000, vmp00sm, vmp00pm, vmp00sf, vmp00pf"
v_tags = v_tags.split(',')

create_generic_entries(v_tags, 'v_np*_le', 'v')