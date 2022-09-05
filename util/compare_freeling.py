import sys
from pathlib import Path


old_freeling_dict_files = sorted(Path(sys.argv[1]).glob('**/MM.*'))
new_freeling_dict_files = sorted(Path(sys.argv[2]).glob('**/MM.*'))

old_names = [f.name for f in old_freeling_dict_files]
new_names = [f.name for f in new_freeling_dict_files]

assert old_names == new_names

for freeling_dict_file in Path(sys.argv[1]).glob('**/MM.*'):
    with open(freeling_dict_file, 'r') as old_v:
        old_v_lines = old_v.readlines()

with open(sys.argv[2], 'r') as new_v:
    new_v_lines = new_v.readlines()

print(5)