import sys
from pathlib import Path
import editdistance

TAGS = 'tags'
SURFACES = 'surfaces'

def process_freeling_file(f, data):
    k = f.suffix[1:]
    data[k] = {TAGS:{}, SURFACES:{}}
    with open(f, 'r') as old_v:
        lines = old_v.readlines()
    for ln in lines:
        surface, lemma, tag = ln.split()
        if not surface in data[k][SURFACES]:
            data[k][SURFACES][surface] = []
        data[k][SURFACES][surface].append(tag)
        if not tag in data[k][TAGS]:
            data[k][TAGS][tag] = []
        data[k][TAGS][tag].append(surface)
    return data

def find_match(t):
    forms = new_version[pos][TAGS][t]
    max = (0, None, 1000)
    for form in forms:
        if form in old_version[pos][SURFACES]:
            old_tags = old_version[pos][SURFACES][form]
            for ot in old_tags:
                oforms = old_version[pos][TAGS][ot]
                isect = len(set(forms).intersection(oforms))/len(set(forms))
                ed = editdistance.eval(ot, t)
                if isect >= max[0] and ed <= max[2]:
                    max = (isect, ot, ed)
        else:
            print('Form {} not found'.format(form))
    return max


old_version = {}
new_version = {}

old_freeling_dict_files = sorted(Path(sys.argv[1]).glob('**/MM.*'))
new_freeling_dict_files = sorted(Path(sys.argv[2]).glob('**/MM.*'))

old_names = [f.name for f in old_freeling_dict_files]
new_names = [f.name for f in new_freeling_dict_files]

assert old_names == new_names


for dict_file in old_freeling_dict_files:
    process_freeling_file(dict_file, old_version)

for dict_file in new_freeling_dict_files:
    process_freeling_file(dict_file, new_version)

to_update = []



for pos in new_version:
    print(pos)
    for tag in new_version[pos][TAGS]:
        if not tag in old_version[pos][TAGS]:
            (confidence, matching_tag, edist) = find_match(tag)
            to_update.append('{}->{} with confidence {}'.format(matching_tag, tag, confidence))

print(len(to_update))

with open('to_update', 'w') as f:
    for tag in to_update:
        f.write(tag + '\n')