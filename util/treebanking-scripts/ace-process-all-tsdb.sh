#!/bin/bash

# Run ACE on every treebank in a directory, parsing the yy-tokens field instead of the raw sentence string.
# This means, the sentence was preprocessed such that it was tokenized and potentially POS-tagged.

directory="$1"

for profile in "$directory"/*; do
  echo $profile
  delphin process --options="-p -y --yy-rules --max-chart-megabytes=24000 --max-unpack-megabytes=36000 --timeout=20" -g ~/delphin/SRG/grammar/srg-agr-divorce/ace/srg.dat --select i-tokens "$profile"
done

