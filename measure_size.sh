#!/bin/bash

# Step 1: Create a virtual environment
python -m venv myenv

# Step 2: Activate the virtual environment
source myenv/bin/activate

# Step 3: Install the dependencies
pip install -r requirements.txt

# Step 4: Check the space used
du -sh myenv

# Step 5: Deactivate the virtual environment
deactivate

# Step 6: Remove the virtual environment
rm -rf myenv