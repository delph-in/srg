import sys
from delphin import ace

with open(sys.argv[1], 'r') as f:
    sentence_list = f.readlines()
grammar = sys.argv[2]
ace_exec = sys.argv[3]
ace_responces = []
no_result = []
with open('ace_err.txt','w') as errf:
    with ace.ACEParser(grammar,cmdargs=['-y','--yy-rules'],executable=ace_exec, stderr=errf) as parser:
        for s in sentence_list:
            response = parser.interact(s)
            if len(response['results']) == 0:
                no_result.append(s)
            ace_responces.append(response)
with open('ace_err.txt', 'r') as errf:
    errors = errf.readlines()
with open('noresults.txt','w') as f:
    for i,nrs in enumerate(no_result):
        f.write(nrs + ': ' + errors[i] + '\n')
