#!/bin/bash

VENV_DIR=".venv"

# create the virtual environment
python3 -m venv $VENV_DIR

# check the operating system
OS=$(uname -s)

# activate the virtual environment based on the OS
if [ "$OS" = "Darwin" ]; then
    # macOS
    source $VENV_DIR/bin/activate
elif [ "$OS" = "Linux" ]; then
    # Linux or WSL
    source $VENV_DIR/bin/activate
else
    # Windows (Git Bash or WSL)
    source $VENV_DIR/Scripts/activate
fi

# install dependencies
pip install -r requirements.txt

# even though uvicorn is installed, it is not available in the PATH
# so we need to install it manually

# install uvicorn
pip install uvicorn

# go to frontend
cd frontend

# install dependencies
npm install

# build the app
npm run build

# api
cd ..
cd api

# run app with uvicorn
uvicorn api:app --reload
