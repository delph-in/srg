import sys
from delphin import itsdb
import glob


def report_stats(treebanks_path):
    all_sentences = []
    all_accepted = []
    all_rejected = []
    for i, tsuite in enumerate(sorted(glob.iglob(treebanks_path + '/**'))):
        sentences = []
        accepted = []
        rejected = []
        ts = itsdb.TestSuite(tsuite)
        items = list(ts.processed_items())
        #print("{} sentences in corpus {} including possible sentences with no parse.".format(len(items), ts.path.stem))
        for response in items:
            all_sentences.append(response['i-input'])
            sentences.append(response['i-input'])
            # In a thinned parsed forest, results will be empty if the item was not accepted as correct in treebanking.
            if len(response['results']) > 0:
                accepted.append(response['i-input'])
                all_accepted.append(response['i-input'])
                #deriv = response.result(0).derivation()
            else:
                #print('Rejected: {}'.format(response['i-input']))
                rejected.append(response['i-input'])
                all_rejected.append(response['i-input'])
        acc = len(accepted)/len(sentences)
        print('Corpus {} accuracy {} out of {} ({:.2f})'.format(ts.path.stem, len(accepted), len(sentences), acc))
    acc = len(all_accepted) / len(all_sentences)
    print('Total accuracy: {} out of {} ({:.2f})'.format(len(all_accepted), len(all_sentences), acc))


if __name__ == '__main__':
    report_stats(sys.argv[1])