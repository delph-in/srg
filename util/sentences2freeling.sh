################################################################################
# Expected usage should be something like:
# 
# $ bash sentences2freeling.sh sentences.txt
#
# ...where "sentences.txt" is a text file with one sentence in each line.
# You may need to modify the python command to python3,
# depending on your environment.
################################################################################

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

analyze -f es.cfg  <$1 2>/dev/null 
