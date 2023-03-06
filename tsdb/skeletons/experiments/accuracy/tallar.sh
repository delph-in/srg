#! /bin/bash

# per executar-ho: 
#./tallar.sh "gold/morph/pos/pcfg"

exp=$1

## crear train.[01234] i test.[01234] a partir de tots els fitxer que són a orig
cat orig/an*/item | gawk 'BEGIN {i=0} {print $0>"test."i; i=(i+1)%5}'
for fold in 0 1 2 3 4; do
  cat test.[^$fold] >train.$fold
done

# separar train.[01234] i test.[01234] per mides per fer els experiments 
for fold in 0 1 2 3 4; do

  rm -rf $exp/tr$fold $exp/ts$fold
  mkdir $exp/tr$fold
  mkdir $exp/ts$fold

  for mida in 01 02 03 04 05 06 07 08 09 10 11 12 13 14; do

    mkdir $exp/tr$fold/an$mida
    mkdir $exp/ts$fold/an$mida

    cp orig/an01/relations $exp/tr$fold/an$mida
    cp orig/an01/relations $exp/ts$fold/an$mida

    awk -F@ -v m=$mida '{if($12==m+0) print;}' train.$fold > $exp/tr$fold/an$mida/item
    awk -F@ -v m=$mida '{if($12==m+0) print;}' test.$fold > $exp/ts$fold/an$mida/item
  done
done

rm -f train.[01234] test.[01234]

