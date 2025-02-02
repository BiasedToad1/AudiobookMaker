# AudiobookMaker

A tool utilizing [piper-tts](https://github.com/rhasspy/piper) to convert books into audiobooks. Also has a page number remover and text splitter built in.

## Voices

To test the included models, go into the 'Models/' directory and test out the included .wav files.

To use other voices including ones for other languages, download a model and config file from [here](https://github.com/rhasspy/piper/blob/master/VOICES.md), and move it into the 'Models/' directory. When using the program, select 'custom' when selecting a model and then type the name of the model out (ex: en_US-amy-medium).

## Windows

This program utilizes Python, if you do not have python installed the program won't run.

To make sure Python is installed on Windows: Open CMD, and type 'python' and press Enter.
If it is not, you will be taken to the Microsoft Store where you can install Python.

After installing Python, go back to the AudiobookMaker folder and double click RUN.bat

## Linux
``` sh
git clone https://github.com/BiasedToad1/AudiobookMaker.git
cd AudiobookMaker
./run.sh
```
## Multiple Books (Linux Only)

To make multiple audiobooks at once, copy your text files into the 'Multi/' directory, then run the `run.sh` file. If there are multiple files, the audiobooks will go into their own folder in 'completed/'
