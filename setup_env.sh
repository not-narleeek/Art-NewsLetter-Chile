#!/bin/bash
set -e

echo "Creating virtual environment 'myenv'..."
python3 -m venv myenv

echo "Activating 'myenv'..."
source myenv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies from requirements.txt..."
pip install -r backend/requirements.txt

echo "Setup complete! To activate the environment run:"
echo "source myenv/bin/activate"
