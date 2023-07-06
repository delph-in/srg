'''
Go through all types in a TDL file and convert comments into docstrings.
Remove the original comments.
'''

import sys, copy, re
from delphin import tdl

def save_tdl_objects(tdl_objects, filename):
    with open(filename, 'w') as f:
        for event, obj, lineno in tdl_objects:
            if event == 'LineComment':
                #if "--- head-spec-phrase types" in obj:
                #    print('stop')
                if not obj.startswith(';'):
                    f.write('; ' + obj + '\n')
                else:
                    f.write(obj + '\n')
            elif event == 'BlockComment':
                f.write('#|' + obj + '|#\n\n')
            else:
                f.write('\n' + tdl.format(obj) + '\n\n')


'''
Does not fully work! Use at your own risk.
May eat up some tdl!
'''
def convert_comments_to_docstrings(tdl_file):
    output = []
    cur_comment = ''
    is_type_comment = False
    prev = None
    for event, obj, lineno in tdl.iterparse(tdl_file):
        if event == 'LineComment' or event == 'BlockComment':
            cur_comment = cur_comment + obj + '\n'
            cur_ln = lineno
            new_type = obj
            prev = (event, obj, lineno, is_type_comment)
        if event == 'TypeDefinition':
            if cur_comment != '' and lineno == cur_ln + 1:
                ds = cur_comment.strip('\n')
                is_type_comment = True
                prev = (prev[0], prev[1], prev[2], True)
                conj = copy.deepcopy(obj.conjunction)
                new_type = tdl.TypeDefinition(obj.identifier, conj, ds)
                output.append(prev)
                output.append((event, new_type, lineno, False))
                cur_comment = ''
            else:
                new_type = obj
                if cur_comment != '':
                    is_type_comment = False
                cur_comment = ''
        if not is_type_comment:
            output.append((event, new_type, lineno))
    save_tdl_objects(output, 'docstring_output.tdl')

# Unfinished:


# def plain_text_convert(filename, output_filename):
#     output_lines = []
#     with open(filename, 'r') as f:
#         lines = f.readlines()
#     cur = 0
#     cur_comment = ''
#     prev = ''
#     i = 0
#     while i < len(lines):
#         ln = lines[i]
#         while i < len(lines) and (ln.startswith(';') or not ln.strip()): # line is a comment
#             cur_comment = cur_comment + ln
#             prev = ln
#             ln = lines[i+1]
#             i +=1 # comments may be multiline
#         if i < len(lines) - 1:
#             next_ln = lines[i+1]
#             if next_ln.strip() != '' and prev.strip() != '': # if the comment is not followed by a blank line, the comment belongs to the type that follows it
#                 p_i, line_with_period = find_period(i+1, lines)
#                 # create docstring from the preceding comment
#                 docstring = '\n"""' + cur_comment + '"""'
#                 if "crd mono-bot/omni-bot" in docstring:
#                     print('stop')
#                 type_with_docstring = ''.join(lines[i:line_with_period])[:-2] + docstring + '.'
#                 print(type_with_docstring)
#                 docstring = ''
#                 if line_with_period + 1 < len(lines):
#                     i = line_with_period + 1
#             else:
#                 # if the comment does not need to be moved into a docstring, print the contents as is
#                 if cur_comment != '':
#                     print(cur_comment)
#                     cur_comment = ''
#                 print(ln)
#                 if i < len(lines):
#                     i +=1



def find_period(start, lines):
    for i, ln in enumerate(lines[start:]):
        if '.' not in ln:
            continue
        return ln.find('.'), start + i +1 # return the index of the period and the index of the line it was found in

#convert_comments_to_docstrings(sys.argv[1])
plain_text_convert(sys.argv[1], sys.argv[2])