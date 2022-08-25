import sys
from delphin import ace

with open(sys.argv[1], 'r') as f:
    sentence_list = f.readlines()
grammar = sys.argv[2]
ace_responces = []
for s in sentence_list:
    response = ace.parse(grammar, s)
    ace_responces.add(response)