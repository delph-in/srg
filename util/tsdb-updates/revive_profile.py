import sys
from delphin import ace, itsdb
import glob

def read_testsuite(path):
    ts = itsdb.TestSuite(path)
    items = list(ts.processed_items())
    sentences = [item['i-input'] for item in items]
    return sentences


testsuite_path = sys.argv[1]

sentences = read_testsuite(testsuite_path)
with open('srg-mrs.txt','w') as f:
    for s in sentences:
        f.write(s + '\n')
