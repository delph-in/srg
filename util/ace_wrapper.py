import sys
from delphin import ace, itsdb
import glob
import subprocess


def run_with_srg(sentence_list, grammar, ace_exec):
    with open('ace_err.txt', 'w') as errf:
        with ace.ACEParser(grammar, cmdargs=['-y', '--yy-rules'], executable=ace_exec, stderr=errf) as parser:
            for s in sentence_list:
                response = parser.interact(s)
                if len(response['results']) == 0:
                    no_result.append(s)
                ace_responces.append(response)
    with open('ace_err.txt', 'r') as errf:
        errors = errf.readlines()
    with open('noresults.txt', 'w') as f:
        for i, nrs in enumerate(no_result):
            f.write(nrs + ': ' + errors[i] + '\n')

def run_with_erg(path, grammar, ace_exec):
    for i, tsuite in enumerate(sorted(glob.iglob(path + '/**'))):
        ts = itsdb.TestSuite(tsuite)
        items = list(ts.processed_items())
        baseline_responses = []
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
        
def run_script(script_path, arg_path):
    output = subprocess.run("'%s' '%s'" % (script_path, arg_path),shell=True,stdout=subprocess.PIPE)
    return output.stdout.decode('utf-8')

if __name__ == "__main__":
    sentence_file = sys.argv[1]
    grammar = sys.argv[2]
    ace_exec = sys.argv[3]
    ace_responces = []
    no_result = []
    #run_with_erg(path, grammar, ace_exec)
    with open(sentence_file, 'r') as f:
        sentences = f.readlines()
    #run_with_srg(sentences,grammar,ace_exec)
    script_output = run_script('./sentences2freeling.sh', 'debug.txt')
    print(script_output)