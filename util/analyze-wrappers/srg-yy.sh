################################################################################
# Usage:
# 
# $ bash srg-yy.sh
#
# Reads from standard input with one sentence per line. Invokes FreeLing with the
# Spanish configuration, and post-processes the output into DELPH-IN YY format.
#
# srg_freeling2yy.py assumes python3
################################################################################

MYPATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# if one of the commands below fails then set the script exit status $? accordingly
set -o pipefail

# For this script to work properly with the LKB we need the following options:
#   analyze --flush: process each line as an independent sentence
#   python3 -u: unbuffered stdout
#
# In the analyze command we could discard output to stderr (i.e. 2>/dev/null), but
# that seems superflous with our usage of analyze; also, stderr communicates useful
# error messages such as "command not found"
analyze -f es.cfg --flush | python3 -u $MYPATH/srg_freeling2yy.py -
