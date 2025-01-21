#!/bin/bash

# Define paths
VENV_DIR="/code/SimpleIngest/ingest"
SCRIPT_PATH="/code/SimpleIngest/simpleingest.py"
REQUIREMENTS_FILE="/code/SimpleIngest/requirements.txt"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Virtual environment 'ingest' not found. Creating it now..."
    python3 -m venv "$VENV_DIR"
    
    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"
    
    # Install dependencies from requirements.txt
    if [ -f "$REQUIREMENTS_FILE" ]; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r "$REQUIREMENTS_FILE"
    else
        echo "Requirements file not found at $REQUIREMENTS_FILE. Skipping dependency installation."
    fi
else
    echo "Virtual environment 'ingest' found."
    # Activate the virtual environment
    source "$VENV_DIR/bin/activate"
fi

# Run your Python script
if [ -f "$SCRIPT_PATH" ]; then
    echo "Running the Python script..."
    python "$SCRIPT_PATH"
else
    echo "Python script not found at $SCRIPT_PATH. Exiting."
fi

# Deactivate the virtual environment
deactivate

echo "Done."
