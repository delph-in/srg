import glob, sys

from delphin import tdl


def parse_lexicons(lexicons):
    for lexicon in glob.iglob(lexicons + '**'):
        for event, obj, lineno in tdl.iterparse(lexicon):
            if event == 'TypeDefinition':
                new_supertype = tdl.TypeIdentifier('native_le')
                obj.supertypes.append(tdl.TypeIdentifier('native_le'))
                print(5)



parse_lexicons(sys.argv[1])