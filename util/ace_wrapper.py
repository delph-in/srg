import sys
from delphin import ace

with open(sys.argv[1], 'r') as f:
    sentence_list = f.readlines()
grammar = sys.argv[2]
ace_exec = sys.argv[3]
ace_responces = []
with ace.ACEParser(grammar,cmdargs=['-y','--yy-rules'],executable=ace_exec) as parser:
    for s in sentence_list:
        response = parser.interact(s)
        ace_responces.append(response)