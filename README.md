To setup the project environment, you will need to install conda.

to run the changes in conda to create the python environment, you will need to run 
```
source setup.sh
```

This will create a conda environment to manage project dependencies named `djenv`.

To activate the conda environment (after `setup.sh`), use the command:
```
conda activate djenv
```

To run the Django server, navigate to grocerysite folder and run
```
python manage.py runserver
```
