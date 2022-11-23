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
                new_id = add_word_to_typename(obj.identifier, '_native', '_le')
                ds = '' if not obj.docstring else obj.docstring
                conj = copy.deepcopy(obj.conjunction)
                new_type = pydelphin_tdl.TypeDefinition(new_id, conj, ds +
                                                        'This is a native lexical entry type, '
                                                        'for words that are in the lexicon.')
                new_type.conjunction.add(pydelphin_tdl.TypeIdentifier('native_le'))
                updated_letypes.append(new_type)
            updated_letypes.append(obj)
        else:
            updated_letypes.append(obj)
    save_tdl_objects(updated_letypes, 'updated_letypes.tdl')

    updated_lexical_entries = []
    for event, obj, lineno in pydelphin_tdl.iterparse(filepath_lex):
        if event == 'TypeDefinition':
            terms = [add_word_to_typename(obj.identifier, '_native', '_le')]
            terms.extend(obj.conjunction.terms[1:])
            conj = pydelphin_tdl.Conjunction(terms)
            new_type = pydelphin_tdl.TypeDefinition(obj.identifier, conj, obj.docstring)
            updated_lexical_entries.append(new_type)
        else:
            updated_lexical_entries.append(obj)

    save_tdl_objects(updated_lexical_entries, 'updated_lexicon.tdl')


def save_tdl_objects(tdl_objects, filename):
    with open(filename, 'w') as f:
        for obj in tdl_objects:
            if isinstance(obj, str):
                if not obj.startswith(';'):
                    f.write('; ' + obj + '\n\n')
                else:
                    f.write(obj + '\n\n')
            else:
                f.write(pydelphin_tdl.format(obj) + '\n\n')

# print(pydelphin_tdl.format(obj))


def add_word_to_typename(name, word, suffix):
    first_part = name[:len(name)-len(suffix)]
    return pydelphin_tdl.TypeIdentifier(first_part + word + suffix)

update_lexicon(sys.argv[1],sys.argv[2])