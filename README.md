# AudiobookMaker

A tool utilizing [piper-tts](https://github.com/rhasspy/piper) to convert books into audiobooks.

## Windows

This program utilizes Python, if you do not have python installed the program won't run.

To make sure Python is installed on Windows: Open CMD, and type 'python' and press Enter.
If it is not, you will be taken to the Microsoft Store where you can install Python.

After installing Python, go back to the AudiobookMaker folder and double click RUN.bat

## Linux

Required dependencies: `ffmpeg`
``` sh
git clone https://github.com/BiasedToad1/AudiobookMaker.git
cd AudiobookMaker
./run.sh
```
## Multiple Files

To make multiple audiobooks at once, copy your text files into the `Multi/` directory, then run the `multi.bat` file for windows or run the `multi.sh` file for Linux.
The default behavior will be used to create the audiobooks, if you want to change it, open the `unattended.py` file in a text editor and change the parameters at the top of the file.
