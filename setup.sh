# for setting up python environment
# need to install conda package manager 
# https://docs.conda.io/en/latest/miniconda.html

# create conda environment
conda create -n djenv python=38

# activate conda environment
conda init bash
conda activate djenv

# install needed packages
conda install django
conda install pandas
conda install ipython
