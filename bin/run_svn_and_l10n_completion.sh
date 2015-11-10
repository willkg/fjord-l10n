#!/bin/bash

# Run this from the fjord-l10n root directory--not this directory!
#
# Usage: ./bin/run_svn_and_l10n_completion.sh OUTPUTFILE LOCALESDIR
#
# Note, this uses python from your path.

function usage() {
    echo "usage: ./bin/run_svn_and_l10n_completion.sh OUTPUTFILE LOCALEDIR"
    exit 1
}

if [[ $# -lt 2 ]];
then
    echo "Not enough arguments."
    usage
fi

PYTHONBIN=$(which python)
OUTPUTFILE=$1
LOCALEDIR=$2

# Check if LOCALEDIR exists
if [[ ! -e "$LOCALEDIR" ]];
then
    echo "$LOCALEDIR does not exist."
    echo "You'll need to svn checkout or git clone that directory."
    usage
fi

# Update the files in svn as a subshell
(cd "$LOCALEDIR" && svn up)

"$PYTHONBIN" ./bin/l10n_completion.py \
             --output "$OUTPUTFILE" \
             --locale "$LOCALEDIR" \
             --truncate 90
