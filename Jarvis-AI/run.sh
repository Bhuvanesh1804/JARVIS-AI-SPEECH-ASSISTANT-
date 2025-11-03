#!/bin/bash

echo "========================================"
echo "    JARVIS AI Assistant Launcher"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo "Starting JARVIS AI Assistant..."
echo ""

# Run the main GUI application
python3 main.py

if [ $? -ne 0 ]; then
    echo ""
    echo "ERROR: Failed to start JARVIS"
    echo "Please check if all dependencies are installed"
    echo "Run: python3 setup.py"
    read -p "Press Enter to exit..."
fi
