################################################################################
# Expected usage should be something like:
# 
# $ bash srg-yy.sh srg-test.txt
#
# ...where "srg-test.txt" is a text file with one sentence in each line.
# Make sure you have the correct path to your srg.dat (or whatever your ACE-compiled
# grammar is called). You may need to modify the python command to python3,
# depending on your environment.
################################################################################

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

analyze -f es.cfg  <$1 2>/dev/null | python $MYPATH/srg-freeling2yy.py | ace -g ../srg.dat -y --yy-rules
