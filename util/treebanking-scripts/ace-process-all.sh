#!/bin/bash

# Run ACE on every treebank in a directory, parsing the yy-tokens field instead of the raw sentence string.
# This means, the sentence was preprocessed such that it was tokenized and potentially POS-tagged.

directory="$1"

for profile in "$directory"/*; do
  echo $profile
  delphin process --options="-y --yy-rules -1" -g ~/delphin/SRG/grammar/srg/ace/srg.dat --full-forest --select i-tokens "$profile"
done

