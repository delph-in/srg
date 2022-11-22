import glob, sys
import copy
from delphin import tdl as pydelphin_tdl
from gmcs import tdl as matrix_tdl


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
                new_id = pydelphin_tdl.TypeIdentifier(obj.identifier + '_native')
                ds = '' if not obj.docstring else obj.docstring
                conj = copy.deepcopy(obj.conjunction)
                new_type = pydelphin_tdl.TypeDefinition(new_id, conj, ds +
                                                        'This is a native lexical entry type, '
                                                        'for words that are in the lexicon.')
                new_type.conjunction.add(pydelphin_tdl.TypeIdentifier('native_le'))
                updated_letypes.append(new_type)
            updated_letypes.append(obj)
    with open('updated_letypes.tdl', 'w') as f:
        for obj in updated_letypes:
            f.write(pydelphin_tdl.format(obj) + '\n\n')



    # with open(filepath_lex, 'r') as f:
    #     lexicon_text = f.read()
    # with open(filepath_letypes, 'r') as f:
    #     letypes_text = f.read()
    # entries = lexicon_text.split('\n\n') # Assume that the entries in the lexicon are separated by two newlines
    # updated_lexicon = matrix_tdl.TDLfile('lexicon-updated.tdl')
    # updated_letypes = matrix_tdl.TDLfile('letypes-updated.tdl')
    # for e in entries:
    #     print(e)
    #     if e.strip():
    #         e_norm = e.strip() # remove any remaining trailing newlines
    #         if not e_norm.startswith(';'):
    #             updated_lexicon.add(e_norm)
    #             supertype_name = e_norm.split(':=')[1].strip().split('&')[0].strip()
    #         else:
    #             updated_lexicon.add_literal(e_norm)
    # updated_lexicon.save()

update_lexicon(sys.argv[1],sys.argv[2])