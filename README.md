Script to prepare pdf digest of github issues using the gh cli and latex.

Requrements:
 - Latex
 - latexmk
 - conda (e.g miniconda)

To run, edit the parse_minutes.sh to replace the `PATH_TO_CLONED_REPO` placeholder with
the path to the cloned FCC action item repository https://github.com/fcccollab/fcc-action-items 

To process an updated pdf of the issues / action items do

```
bash parse_minutes.sh
```

if a conda environment is not found, the script will set one up with Python and the GitHub CLI. The issues are extract and populated into the template in `latex_tempate` and stored in the `pdfs` with a name corresponding to the current date.

