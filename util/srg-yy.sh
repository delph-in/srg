################################################################################
# Expected usage should be something like:
# 
# $ bash srg-yy.sh srg-test.txt
# (where "srg-test.txt" is a text file with one sentence in each line)
################################################################################

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

analyze -f es.cfg  <$1 2>/dev/null | python $MYPATH/srg-freeling2yy.py | ace -g ../srg.dat -y --yy-rules
