#!/bin/bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pyinstaller --name AudiobookMaker --windowed --collect-all piper --collect-all onnxruntime AudiobookMaker.py
mkdir -p app/usr/bin
cp -r dist/AudiobookMaker/* app/usr/bin/
wget https://github.com/AppImage/appimagetool/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
ARCH=x86_64 ./appimagetool-x86_64.AppImage app
