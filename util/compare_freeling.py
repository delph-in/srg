import sys
from pathlib import Path

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

def find_match():
    forms = new_version[pos][TAGS][tag]
    for form in forms:
        if form in old_version[pos][SURFACES]:
            old_tags = old_version[pos][SURFACES][form]
            for ot in old_tags:
                oforms = old_version[pos][TAGS][ot]
                isect = len(set(forms).intersection(oforms))/len(set(forms))
                if isect > 0.5:
                    return ot, isect
        else:
            print('Form {} not found'.format(form))


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
            matching_tag, confidence = find_match()
            to_update.append('{}->{} with confidence {}'.format(matching_tag, tag, confidence))

print(len(to_update))

with open('to_update', 'w') as f:
    for tag in to_update:
        f.write(tag + '\n')