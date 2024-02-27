#!/usr/bin/env bash

# Script to parse action item list from GitHub issues
# and create a pdf digest
# Requirements:
# - Miniconda (https://educe-ubc.github.io/conda.html) or equivalent
# - Latex and latexmk

# FCC_ACTION_REPO_PATH="PATH_TO_CLONED_REPO" # Repository: https://github.com/fcccollab/fcc-action-items

# check that the FCC action repo path exists and exit with an error if not
if [ ! -d $FCC_ACTION_REPO_PATH ]; then
    echo "FCC action repo path does not exist: $FCC_ACTION_REPO_PATH"
    exit 1
fi

# Activate conda and prepare the environment
eval "$(conda shell.bash hook)"
CONDA_BASE=$(conda info --base)
CONDA_PATH=${CONDA_BASE%/envs/*}
echo 'Conda installed in '$CONDA_BASE
source $CONDA_PATH'/etc/profile.d/conda.sh'
source $CONDA_PATH'/bin/activate'

CONDA_GH_ENV='gh_client'

# If it doesn't exist, create a miniconda environment with gh and latexmk packages, with conda-forge set as the default channel
if [ ! -d "$CONDA_PATH/envs/$CONDA_GH_ENV" ]; then
    echo "Creating conda environment '$CONDA_GH_ENV'"
    conda create -n "$CONDA_GH_ENV" -c conda-forge --yes python=3.9 gh=2.9 pandas=1.4
else
    echo "Using existing conda environment '$CONDA_GH_ENV'"
fi

conda activate $CONDA_GH_ENV

# The analysis path is the directory of this script
ANALYSISPATH=$( cd $(dirname $0) ; pwd -P )
LATEXBUILDPATH=$ANALYSISPATH/'latex_build'
PDFPATH=$ANALYSISPATH/'pdfs'

TEXNAMESTUB='action-item-list'
TEXLOGFILE='latexmk_output.log'
PDFNAMESTUB='FCC-action-items-'

cd $FCC_ACTION_REPO_PATH

gh issue list --limit 1000 --state all | tr '\t' ';' > $ANALYSISPATH/issues.csv
if [ $? -ne 0 ]; then
    echo "Encountered an issue parsing the action items - wrong repository path?"
    exit 1
fi

cd $ANALYSISPATH

python format_issues.py

cd $LATEXBUILDPATH
latexmk -pdf $TEXNAMESTUB > $TEXLOGFILE && latexmk -c $TEXNAMESTUB
cd $ANALYSISPATH

DATE=$(date '+%Y-%m-%d')
cp $LATEXBUILDPATH/$TEXNAMESTUB.pdf $PDFPATH/$PDFNAMESTUB$DATE.pdf

echo "Prepared file "$PDFPATH/$PDFNAMESTUB$DATE.pdf

# clean up
rm $ANALYSISPATH/issues.csv
#rm $LATEXBUILDPATH/* # clean up latex files, done thorough latexmk


conda deactivate
