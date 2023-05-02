#!/bin/bash

# Run ACE on an treebank parsing the yy-tokens field instead of the raw sentence string.
# This means, the sentence was preprocessed such that it was tokenized and potentially POS-tagged.

profile="$1"

delphin process --options="-y --yy-rules -1" -g ~/delphin/SRG/grammar/srg/ace/srg.dat --full-forest --select i-tokens ~/delphin/SRG/treebanks/dev/all/$profile
