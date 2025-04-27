#!/bin/bash

# Create a new virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "MISTRAL_API_KEY=your_api_key_here" > .env
    echo "Created .env file. Please update it with your Mistral API key."
fi

echo "Environment setup complete! Don't forget to:"
echo "1. Activate the environment with: source venv/bin/activate"
echo "2. Update the .env file with your Mistral API key" 