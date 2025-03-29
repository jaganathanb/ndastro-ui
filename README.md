# ndastro-ui

`ndastro-ui` is a user interface project designed for astronomical data analysis. This project leverages Python and various libraries to provide a seamless experience for users working with astronomical datasets.

## Setting up environments

1. Ensure `pyenv-win` is installed and configured.
2. Install the required Python version with `pyenv install <version>`.
3. Set the installed version as the local version for the workspace with `pyenv local <version>`.
4. Create the pyproject.toml file by running the `poetry init` cmd.
5. Create the virtual environment with `poetry env use <python version>`.
6. Install the necessary packages for app development with `poetry add <package>` or `poetry install` if dependencies are already listed.
7. If you get Import errors make sure that the you have the python interpreter selected properly. Since we use poetry and pyenv, the     interpreter should be from AppData\Local\pypoetry\Cache\virtualenvs\<virtual env name>\Scripts\python.exe. i.e the virtula env you have created using pyenv - ndastro-ui-zXewb6rb-py3.13

## Convert resources to python objects
You can convert the resources to python objects which could be easily bundled and access in the app.
`pyside6-rcc .\resources.qrc -o resources.py`