#!/bin/bash
if [ -f INPUT_TEXT.txt ]; then 
    source .venv/bin/activate
    python3 main.py
else
    echo "Please use directory \"AudiobookMaker/\""
fi