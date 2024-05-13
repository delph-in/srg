import sys
from delphin import itsdb, derivation
import glob
import os


# Open two folders containing different versions of the same treebanks. Report the differences between them.
def compare_treebanks(old_path, new_path):
    identical = True
    old_treebanks = {}
    new_treebanks = {}
    ot_path = sorted(glob.iglob(old_path + '/**'))
    nt_path = sorted(glob.iglob(new_path + '/**'))
    for old_tsuite, new_tsuite in zip(ot_path, nt_path):
        add_to_dict(old_treebanks, old_tsuite)
        add_to_dict(new_treebanks, new_tsuite)
    # Iterate over two dictionaries comparing key names and number of items in each key.
    if old_treebanks.keys() == new_treebanks.keys():
        for (old_folder, old_items), (new_folder, new_items) in zip(old_treebanks.items(), new_treebanks.items()):
            if len(old_items) == len(new_items):
                print('\nCollecting parsed items from {}'.format(old_folder))
                old_responses = collect_parsed(old_items)
                new_responses = collect_parsed(new_items)
                # Given two lists of parsed items, compare the results of items with the same id.
                for old_response, new_response in zip(old_responses, new_responses):
                    o_derivs = []
                    n_derivs = []
                    if old_response['i-id'] == new_response['i-id']:
                        orr = old_response['results']
                        nrr = new_response['results']
                        for o, n in zip(orr, nrr):
                            o_deriv = derivation.from_string(o['derivation'])
                            n_deriv = derivation.from_string(n['derivation'])
                            if o_deriv not in o_derivs:
                                o_derivs.append(o_deriv)
                            if n_deriv not in n_derivs:
                                n_derivs.append(n_deriv)
                            if o_deriv != n_deriv:
                                print('Differences found in item {}: {}'.format(old_response['i-id'], old_response['i-input']))
                                identical = False
                        if len(orr) != len(nrr):
                            identical = False
                            print('item {}: {} results in old version, {} results in new version'.format(
                                old_response['i-id'], len(orr), len(nrr)))
    else:
        identical = False
    if identical:
        print('No differences found between treebanks')


def add_to_dict(treebanks, tsuite):  # Process items of a tsuite and stores them in a dictionary.
    folder = os.path.basename(tsuite)
    if folder not in treebanks.keys():
        treebanks[folder] = []
    ts = itsdb.TestSuite(tsuite)
    treebanks[folder] = list(ts.processed_items())


#Iterate over a list of responses, storing them in a list if their attribute ['results'] is not empty.
def collect_parsed(items):
    parsed_items = []
    for response in items:
        if len(response['results']) > 0:
            parsed_items.append(response)
    return parsed_items

if __name__ == '__main__':
    compare_treebanks(sys.argv[1], sys.argv[2])
