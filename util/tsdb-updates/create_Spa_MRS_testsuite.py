'''
Assuming a [incr tsdb()] profile created with pydelphin from a text file
and a textfile mapping the same sentences from the text file to ID numbers,
update the test suite to use those id numbers instead of the automatically created ones.
'''
import sys
from delphin import itsdb

def get_id_mappings(file_ids):
    sentence2id = {}
    with open (file_ids, 'r') as f:
        sentences_ids = [ln  for ln in f.read().splitlines() if ln]
        for s_id in sentences_ids:
            id,s = s_id.split('\t')
            sentence2id[s] = int(id)
    return sentence2id
def update_ids(ts_path, id_mappings):
    ts = itsdb.TestSuite(ts_path)
    for i, row in enumerate(ts['item']):
        id = id_mappings[ts['item'][i]['i-input']]
        ts['item'].update(i, {'i-id':id})
    ts.commit() # ts is a database which needs to be committed to disk, otherwise the updates will not persist.


if __name__ == "__main__":
    id_mappings = get_id_mappings(sys.argv[2])
    update_ids(sys.argv[1], id_mappings)