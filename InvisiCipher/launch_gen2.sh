#!/bin/bash

echo "================================================"
echo "InvisiCipher Gen2 Launcher (Unix/Linux)"
echo "================================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Python found. Starting launcher..."
echo

# Run the Python launcher
python3 launch_gen2.py

# Check exit status
if [ $? -ne 0 ]; then
    echo
    echo "Launcher failed with error code $?"
    read -p "Press Enter to continue..."
fi
