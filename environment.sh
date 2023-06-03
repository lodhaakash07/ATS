#!/bin/bash

# Check if the virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    # Check if the virtual environment directory exists
    if [[ ! -d "venv" ]]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
        source venv/bin/activate
    fi

    echo "Activating the virtual environment..."
    source venv/bin/activate
fi

# Check if required packages are installed
if ! cmp --silent requirements.txt <(pip freeze); then
    echo "Installing missing packages..."
    pip install -r requirements.txt
    source venv/bin/activate
fi
