################################################################################
# Usage:
# 
# $ bash srg-yy-python-api.sh
#
# Reads from standard input with one sentence per line. Invokes FreeLing with the
# Spanish configuration, and post-processes the output into DELPH-IN YY format.
#
# Assumes python3
################################################################################

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $MYPATH

# if one of the commands below fails then set the script exit status $? accordingly
set -o pipefail

python3 -u $MYPATH/freeling2lkb.py -
