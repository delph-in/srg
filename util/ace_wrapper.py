import sys
from delphin import ace, itsdb
import glob
from srg_freeling2yy import convert_sentences
from populate_tokens import run_script, read_testsuite

def run_with_srg(ts, grammar, ace_exec):
    responces = []
    no_result = []
    sentence_list = read_testsuite(ts)
    script_output = run_script('./sentences2freeling.sh', sentence_list)
    yy = convert_sentences(script_output)
    assert len(yy) == len(ts['item'])
    for i, row in enumerate(ts['item']):
        ts['item'].update(i, {'i-tokens': yy[i]})
    #ts['item'].update(7,yy)
    ts.commit()
    with open('ace_err.txt', 'w') as errf:
        with ace.ACEParser(grammar, cmdargs=['-y', '--yy-rules'], executable=ace_exec, stderr=errf) as parser:
            for s in yy:
                response = parser.interact(s)
                if len(response['results']) == 0:
                    no_result.append(s)
                responces.append(response)
    with open('ace_err.txt', 'r') as errf:
        errors = errf.readlines()
    with open('noresults.txt', 'w') as f:
        for nrs in no_result:
            f.write(nrs+'\n')
    return responces, no_result

def run_with_erg(path, grammar, ace_exec):
    for i, tsuite in enumerate(sorted(glob.iglob(path + '/**'))):
        ts = itsdb.TestSuite(tsuite)
        items = list(ts.processed_items())
        baseline_responses = []
        no_result = []
        with open('ace_err.txt', 'w') as errf:
            with ace.ACEParser(grammar, executable=ace_exec, stderr=errf) as parser:
                for response in items:
                    # Reparse each sentence, to measure the parser speed without supertagging
                    baseline_response = parser.interact(response['i-input'])
                    if len(baseline_response['results']) == 0:
                        no_result.append(response['i-input'])
                    else:
                        baseline_responses.append(response)
        with open('ace_err.txt', 'r') as errf:
            errors = errf.readlines()
        with open('noresults.txt', 'w') as f:
            for i, nrs in enumerate(no_result):
                f.write(nrs + ': ' + errors[i] + '\n')
        return baseline_responses


if __name__ == "__main__":
    ts = itsdb.TestSuite(sys.argv[1])
    grammar = sys.argv[2]
    ace_exec = sys.argv[3]
    parses, no_parses = run_with_srg(ts, grammar, ace_exec)
    assert len(parses) == len(ts['item'])
<<<<<<< HEAD
    print('done')
=======
    #ts['result'] = parses
    #fm = itsdb.FieldMapper(ts)
    #for p in parses:
    #    fm.map(p)
    print('done')
>>>>>>> 919419403d06992bd1a676e1fcda055c132abd87
