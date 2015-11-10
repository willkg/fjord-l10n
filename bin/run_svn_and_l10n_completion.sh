#!/bin/bash

# Run this from the fjord-l10n root directory--not this directory!
#
# Usage: ./bin/run_svn_and_l10n_completion.sh PYTHONBIN OUTPUTFILE LOCALESDIR

function usage() {
    echo "usage: ./bin/run_svn_and_l10n_completion.sh PYTHONBIN OUTPUTFILE LOCALESDIR"
    exit 1
}

if [[ $# -lt 3 ]];
then
    echo "Not enough arguments."
    usage
fi

PYTHONBIN=$1
OUTPUTFILE=$2
LOCALESDIR=$3

# Check if LOCALESDIR exists
if [[ ! -e "$LOCALESDIR" ]];
then
    echo "$LOCALESDIR does not exist."
    usage
fi

# Update the files in svn as a subshell
(cd "$LOCALESDIR" && svn up)

"$PYTHONBIN" ./bin/l10n_completion.py \
             --output "$OUTPUTFILE" \
             --locales "$LOCALESDIR" \
             --truncate 90
