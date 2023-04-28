#!/bin/bash
# This script moves the contents of each pet subfolder into the parent folder, e.g. tbdb01/


for dir in /home/olga/delphin/SRG/treebanks/old-gold/tbdb*/pet/; do
  parent=$(dirname "$dir")
  cd "$parent"
  mv "$dir"/* .
  rm -r "$parent"/pet
done

