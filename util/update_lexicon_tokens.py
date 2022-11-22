import glob, sys

#from delphin import tdl
from gmcs import tdl


def parse_lexicons(filepath):
    with open(filepath, 'r') as f:
        lexicon_text = f.read()
    entries = lexicon_text.split('\n\n') # Assume that the entries in the lexicon are separated by two newlines
    updated_lexicon = tdl.TDLfile('lexicon-updated.tdl')
    for e in entries:
        print(e)
        if e.strip():
            e_norm = e.strip() # remove any remaining trailing newlines
            if not e_norm.startswith(';'):
                updated_lexicon.add(e_norm)
                type_name = e_norm.split(':=')[0].strip()
                updated_lexicon.add(type_name + ':= [ TRAITS native_token_list ].',merge=True)
            else:
                updated_lexicon.add_literal(e_norm)
    updated_lexicon.save()


parse_lexicons(sys.argv[1])