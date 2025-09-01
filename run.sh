#!/bin/bash
if [ -d "piper" ]; then 
    python3 main.py
else
    echo "Please use directory \"AudiobookMaker/\""
fi