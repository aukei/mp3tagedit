#!/bin/bash
# Installation script for MP3 Tag Editor

echo "Installing MP3 Tag Editor dependencies..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "pip3 is not installed. Installing pip..."
    python3 -m ensurepip --upgrade
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

echo "Installation complete!"
echo "You can now run the application with: ./mp3tagedit.py"