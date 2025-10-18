# AudiobookMaker

A tool utilizing [piper-tts](https://github.com/rhasspy/piper) to convert books into audiobooks. Also has a page number remover and text splitter built in.

## Voices

To test different voice models, use [this website](https://rhasspy.github.io/piper-samples/).

To use other voices including ones for other languages, download a model and config file from [here](https://github.com/rhasspy/piper/blob/master/VOICES.md), and move it into the 'models/' directory. When using the program, select 'custom' when selecting a model and then type the name of the model out (ex: en_US-amy-medium).

## Linux
Requirements
```
python
```
In a terminal, run these commands to install AudiobookMaker:
``` sh
git clone https://github.com/BiasedToad1/AudiobookMaker.git
cd AudiobookMaker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Run using:
```sh
./run.sh
```

## Windows

> [!WARNING]
> Windows support has been dropped. Please use the latest windows release for last working version

This program utilizes Python, if you do not have python installed the program won't run.

To make sure Python is installed on Windows: Open CMD, and type 'python' and press Enter.
If it is not, you will be taken to the Microsoft Store where you can install Python.

After installing Python, install the [latest windows release](https://github.com/BiasedToad1/AudiobookMaker/releases/download/tts/AudiobookMakerWindows.zip), unzip it, double click RUN.bat

## Multiple Books (Linux Only)

To make multiple audiobooks at once, copy your text files into the 'Multi/' directory, then run the `run.sh` file. If there are multiple files, the audiobooks will go into their own folder in 'completed/'
