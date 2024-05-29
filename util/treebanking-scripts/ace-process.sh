#!/bin/bash

# Run ACE on an treebank parsing the yy-tokens field instead of the raw sentence string.
# This means, the sentence was preprocessed such that it was tokenized and potentially POS-tagged.

profile="$1"

delphin process --options="-1 -p -y --yy-rules --max-chart-megabytes=48000 --max-unpack-megabytes=56000" -g ~/delphin/SRG/grammar/srg/ace/srg.dat --full-forest --select i-tokens $profile
