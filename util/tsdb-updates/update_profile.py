'''
This script helps update outdated [incr tsdb()] profiles, which miss some columns in some files.
To add new empty columns, for example, to turn

1@@gcc 3.4@1@2.0 (23-jun-13; beta)@PET(tom cheap v0.99.14svn_cm) [... more things here ] @complete

into

1@@gcc 3.4@1@2.0 (23-jun-13; beta)@@PET(tom cheap v0.99.14svn_cm) [... more things here ] @complete

...in the file called "run", you need to run this script as follows:

python3 update_profile.py file-to-testuite-folder/run 4

This means insert an @ sign into the fourth position, as the fourth column.

You can also use the script to insert more than one @ at the same time, but be careful:
if you need to insert several @ signs in a row, you need to ask for them to be inserted in the same position,
e.g.: python3 update_profile.py path-to-testsuite-folder/item 8,8,8. If the positions are not consecutive,
use the actual positions, e.g. 2,5

'''


import sys

def find_all(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def insert_at(filepath, positions):
    with open(filepath, 'r') as f:
        items = f.readlines()
    updated = []
    for item in items:
        updated_item = item
        for i,pos in enumerate(positions):
            indices = find_all(updated_item,'@')
            assert len(indices) >= pos-1+i
            updated_item = updated_item[:indices[pos-1+i]]+'@'+ updated_item[indices[pos-1+i]:]
        updated.append(updated_item)
    with open(filepath+'updated', 'w') as f:
        for updated_item in updated:
            f.write(updated_item)


fp = sys.argv[1]
positions = [ int(n) for n in sys.argv[2].split(',') ]

insert_at(fp, positions)

# insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/run',[4])
# insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/parse',[24,24,24,24,24])
# insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/edge',[8])
# insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/score',[3,3,3,3])
# insert_at('/Users/olzama/Research/delphin/Marimon/updated-tsdb/mrs/item',[8,8,8])