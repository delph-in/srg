'''
Go through all types in a TDL file and convert comments into docstrings.
Remove the original comments.
'''

import sys, copy
from delphin import tdl

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
                f.write('\n' + tdl.format(obj) + '\n\n')


def convert_comments_to_docstrings(tdl_file):
    output = []
    cur_comment = ''
    is_type_comment = False
    for event, obj, lineno in tdl.iterparse(tdl_file):
        if event == 'LineComment' or event == 'BlockComment':
            cur_comment = cur_comment + obj + '\n'
            cur_ln = lineno
            new_type = obj
        if event == 'TypeDefinition':
            if cur_comment != '' and lineno == cur_ln + 1:
                ds = cur_comment.strip('\n')
                is_type_comment = True
                conj = copy.deepcopy(obj.conjunction)
                new_type = tdl.TypeDefinition(obj.identifier, conj, ds)
                output.append((event, new_type, lineno))
                cur_comment = ''
            else:
                new_type = obj
                if cur_comment != '':
                    is_type_comment = False
                cur_comment = ''
        if not is_type_comment:
            output.append((event, new_type, lineno))
    save_tdl_objects(output, 'docstring_output.tdl')


convert_comments_to_docstrings(sys.argv[1])