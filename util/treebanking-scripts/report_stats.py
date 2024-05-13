import sys
from delphin import itsdb
import glob


def report_stats(treebanks_path):
    all_sentences = []
    all_accepted = []
    all_rejected = []
    all_overgenerated = []
    all_illformed = []
    for i, tsuite in enumerate(sorted(glob.iglob(treebanks_path + '/**'))):
        sentences = []
        accepted = []
        rejected = []
        overgenerated = []
        illformed = []
        ts = itsdb.TestSuite(tsuite)
        items = list(ts.processed_items())
        #print("{} sentences in corpus {} including possible sentences with no parse.".format(len(items), ts.path.stem))
        for response in items:
            all_sentences.append(response['i-input'])
            sentences.append(response['i-input'])
            # In a thinned parsed forest, results will be empty if the item was not accepted as correct in treebanking.
            if len(response['results']) > 0:
                if response['i-wf'] == 1:
                    accepted.append(response['i-input'])
                    all_accepted.append(response['i-input'])
                else:
                    overgenerated.append(response['i-input'])
                    all_overgenerated.append(response['i-input'])
                    illformed.append(response['i-input'])
                #deriv = response.result(0).derivation()
            else:
                #print('Rejected: {}'.format(response['i-input']))
                if response['i-wf'] == 0:
                    illformed.append(response['i-input'])
                    all_illformed.append(response['i-input'])
                rejected.append(response['i-input'])
                all_rejected.append(response['i-input'])
        acc = len(accepted)/(len(sentences) - len(illformed))
        overgen = len(overgenerated)/len(illformed) if len(illformed) > 0 else 0
        print('Corpus {} accuracy {} out of {} ({:.4f})'.format(ts.path.stem, len(accepted), len(sentences)-len(illformed), acc))
        #print('Corpus {} overgeneration {} out of {} ({:.4f})'.format(ts.path.stem, len(overgenerated), len(illformed), overgen))
    acc = len(all_accepted) / (len(all_sentences) - len(all_illformed))
    overgen = len(all_overgenerated) / len(all_illformed) if len(all_illformed) > 0 else 0
    print('Total accuracy: {} out of {} ({:.4f})'.format(len(all_accepted), len(all_sentences)-len(all_illformed), acc))
    #print('Total overgeneration: {} out of {} ({:.4f})'.format(len(all_overgenerated), len(all_illformed), overgen))


if __name__ == '__main__':
    report_stats(sys.argv[1])