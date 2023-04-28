#!/bin/bash

# This script runs the fftb treebanker tool without loading a second profile as the "gold" one.

profile="$1"


fftb -g ~/delphin/SRG/grammar/srg/ace/srg.dat --browser --webdir ~/delphin/tools/acetools/assets/ ~/delphin/SRG/treebanks/dev/processed/$profile
