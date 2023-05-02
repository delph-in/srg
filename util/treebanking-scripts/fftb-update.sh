#!/bin/bash

# Run the treebanker tool with a second profile (gold), enabling a partial automatic update

profile="$1"

fftb -g ~/delphin/SRG/grammar/srg/ace/srg.dat --browser --webdir ~/delphin/tools/acetools/assets/ --gold ~/delphin/SRG/treebanks/dev/gold/$profile ~/delphin/SRG/treebanks/dev/processed/$profile
