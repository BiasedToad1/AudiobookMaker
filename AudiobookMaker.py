import sys
import os
import wave
from piper import PiperVoice
from piper.download_voices import download_voice
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMessageBox,
    QPlainTextEdit,
    QPushButton,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
    QComboBox,
)

def removePageNums(tempLine):
    pgs = 0 # keeps pg count
    try:
        for i in range(0, len(tempLine) - 2): # scans through tempLine to look for pg nums
            if (tempLine[i] in '123456789') and (i == 0 or tempLine[i - 1] == '\n'):
                if tempLine[i + 1] == '\n': # 1 digit nums
                    tempLine = tempLine[:i] + ' ' + tempLine[i + 1:]
                    pgs += 1
                elif (tempLine[i + 1] in '1234567890,'):
                    if tempLine[i + 2] == '\n': # 2 digit nums
                        tempLine = tempLine[:i] + '  ' + tempLine[i + 2:]
                        pgs += 1
                    elif (tempLine[i + 2] in '1234567890'):
                        if tempLine[i + 3] == '\n': # 3 digit nums
                            tempLine = tempLine[:i] + '  ' + tempLine[i + 3:]
                            pgs += 1
                        elif (tempLine[i + 3] in '123456789'):
                            if tempLine[i + 4] == '\n': # 4 digit nums
                                tempLine = tempLine[:i] + '  ' + tempLine[i + 4:]
                                pgs += 1
                            elif (tempLine[i + 4] in '123456789' and tempLine[i + 5] == '\n'): # 4 digit nums w/ comma
                                tempLine = tempLine[:i] + '  ' + tempLine[i + 5:]
                                pgs += 1
    except IndexError:
        pass
    print(f"Page Numbers Deleted: {pgs}")
    return tempLine

def findAndDelete(tempLine, find):
    tempLine.replace(find, " ")
    if not find:
        return tempLine
    return tempLine.replace(find, "")

def modelDownloader(modelChoice, qualityChoice):
    folder = Path.home() / ".local" / "share" / "AudiobookMaker"
    folder.mkdir(parents=True, exist_ok=True)
    # if not os.path.exists(f"~/.local/share/AudiobookMaker/en_US-{modelChoice}-{qualityChoice}.onnx"):
    #     os.system(f"cd ~/.local/share/AudiobookMaker && python3 -m piper.download_voices en_US-{modelChoice}-{qualityChoice}")
    model_file = folder / f"en_US-{modelChoice}-{qualityChoice}.onnx"
    if not model_file.exists():
        # os.system(f"cd {folder} && python3 -m piper.download_voices en_US-{modelChoice}-{qualityChoice}")
        download_voice(f"en_US-{modelChoice}-{qualityChoice}", folder)

def renderAudiobook(text, model, quality, path):
    print("model: " + model + "\npath: " + path)
    modelPath = Path.home() / ".local" / "share" / "AudiobookMaker" / f"en_US-{model}-{quality}.onnx"
    voice = PiperVoice.load(str(modelPath))
    with wave.open(str(Path(path) / "Audiobook.wav"), "wb") as wav_file:
        voice.synthesize_wav(text, wav_file)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AudiobookMaker")
        self.resize(500, 350)

        #first page: upload file (can't go to next until this is done)
        self.status = QLabel("No file loaded")
        self.fileUploadStatus = False
        self.status.setAlignment(Qt.AlignCenter)
        upload_button = QPushButton("Upload file...")
        upload_button.clicked.connect(self.upload_file)

        page1 = QWidget()
        layout1 = QVBoxLayout(page1)
        layout1.addStretch()
        layout1.addWidget(self.status)
        layout1.addWidget(upload_button)
        layout1.addStretch()

        #second page: text editor and tools (page num remover, find and replace)
        self.editor = QPlainTextEdit()
        page2 = QWidget()
        layout2 = QVBoxLayout(page2)
        layout2.addWidget(self.editor)

        pndLayout = QHBoxLayout()
        self.pndDrop = QComboBox()
        self.pndDrop.addItems(["1, 2, 3...", "Page 1, Page 2... (NOT WORKING)", "Custom (NOT WORKING)"])

        #FIX LATER vvvv
        self.pndDrop.model().item(1).setEnabled(False)
        self.pndDrop.model().item(2).setEnabled(False)

        self.pndDrop.currentTextChanged.connect(self.pndOptionChanged)
        pageButton = QPushButton("Delete Page Numbers")
        pndLayout.addWidget(self.pndDrop)
        pndLayout.addWidget(pageButton)

        pageButton.clicked.connect(self.onPND)

        fadLayout = QHBoxLayout()
        self.fadEdit = QPlainTextEdit()
        self.fadEdit.setMaximumHeight(30)
        self.fadEdit.setPlaceholderText("Insert text to find")
        fadButton = QPushButton("Find and Delete")
        fadLayout.addWidget(self.fadEdit)
        fadLayout.addWidget(fadButton)

        fadButton.clicked.connect(self.onFAD)

        layout2.addLayout(pndLayout)
        layout2.addLayout(fadLayout)

        # #export
        # export_button = QPushButton("Export file")
        # export_button.clicked.connect(self.export_file)
        # layout2.addWidget(export_button)


        #third page: voice model chooser/downloader
        page3 = QWidget()
        layout3 = QVBoxLayout(page3)

        self.modelStatus = False
        self.modelChoice = ""
        self.qualityChoice = ""

        self.downloadModelButton = QPushButton("Download Model")
        self.useModelButton = QPushButton("Use Model")
        self.modelDropdown = QComboBox()
        self.modelDropdown.addItems(["Select Model", "amy", "arctic", "bryce", "danny", "hfc_female", "hfc_male", "joe", "john", "kathleen", "kristin", "kusal", "l2arctic", "lessac", "libritts", "ljspeech", "norman", "reza_ibrahim", "ryan", "sam"])
        self.modelDropdown.currentTextChanged.connect(self.modelOptionChanged)
        self.qualityDropdown = QComboBox()
        self.qualityDropdown.addItems(["Select Quality", "low", "medium", "high"])
        self.qualityDropdown.currentTextChanged.connect(self.qualityOptionChanged)
        self.qualityDropdown.model().item(1).setEnabled(False)
        self.qualityDropdown.model().item(2).setEnabled(False)
        self.qualityDropdown.model().item(3).setEnabled(False)
        self.downloadModelButton.setEnabled(False)
        self.useModelButton.setEnabled(False)
        self.downloadModelButton.clicked.connect(self.downloadModel)
        self.useModelButton.clicked.connect(self.useModel)

        layout3.addWidget(self.modelDropdown)
        layout3.addWidget(self.qualityDropdown)
        layout3.addWidget(self.downloadModelButton)
        layout3.addWidget(self.useModelButton)

        #fourth page: render & export (path)
        page4 = QWidget()
        layout4 = QVBoxLayout(page4)
        self.folderButton = QPushButton("Choose folder")
        self.renderButton = QPushButton("Render")
        self.folderButton.clicked.connect(self.choose_folder)
        self.renderButton.clicked.connect(self.renderProject)
        self.outputFolder = ""
        expText = QLabel("Export:")
        self.renderButton.setEnabled(False)

        layout4.addStretch()
        layout4.addWidget(expText)
        layout4.addWidget(self.folderButton)
        layout4.addWidget(self.renderButton)
        layout4.addStretch()


        #navigation
        self.stack = QStackedWidget()
        self.stack.addWidget(page1)
        self.stack.addWidget(page2)
        self.stack.addWidget(page3)
        self.stack.addWidget(page4)

        self.back_button = QPushButton("Back")
        self.next_button = QPushButton("Next")
        self.back_button.clicked.connect(lambda: self.go(-1))
        self.next_button.clicked.connect(lambda: self.go(1))

        nav = QHBoxLayout()
        nav.addWidget(self.back_button)
        nav.addStretch()
        nav.addWidget(self.next_button)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.stack)
        main_layout.addLayout(nav)
        self.update_buttons()

    def renderProject(self):
        QMessageBox.information(self, "Rendering Project", "Rendering Audiobook Please Wait.")
        renderAudiobook(self.editor.toPlainText(), self.modelChoice, self.qualityChoice, self.outputFolder)
        QMessageBox.information(self, "Rendering Finished", "Project rendering has concluded.")

    def choose_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Choose a folder", str(Path.home()))
        if not path: # user cancelled, so leave the button alone
            return
        self.outputFolder = path
        self.folderButton.setText(path)
        self.renderButton.setEnabled(True)

    def pndOptionChanged(self, text):
        print("Selected:", text)
        # ADD MORE LATER

    def downloadModel(self):
        print(f"Downloading {self.modelChoice}-{self.qualityChoice}")
        modelDownloader(self.modelChoice, self.qualityChoice)
        QMessageBox.information(self, "Model Downloaded", "The model download has completed.")
        self.modelCheck()
        #QMessageBox.information(self, "Download Failed", "The model is already downloaded or failed to download.")

    def useModel(self):
        print(f"Use {self.modelChoice}-{self.qualityChoice}")
        self.modelStatus = True
        self.update_buttons()

    def modelOptionChanged(self, choice):
        print("Selected:", choice)
        if choice == "Select Model":
            self.qualityDropdown.model().item(1).setEnabled(False)
            self.qualityDropdown.model().item(2).setEnabled(False)
            self.qualityDropdown.model().item(3).setEnabled(False)
        else:
            self.qualityDropdown.model().item(1).setEnabled(True)
            self.qualityDropdown.model().item(2).setEnabled(True)
            self.qualityDropdown.model().item(3).setEnabled(True)
            self.modelChoice = choice
        self.modelCheck()

    def modelCheck(self):
        folder = Path.home() / ".local" / "share" / "AudiobookMaker"
        folder.mkdir(parents=True, exist_ok=True)
        model_file = folder / f"en_US-{self.modelChoice}-{self.qualityChoice}.onnx"
        if model_file.exists():
            self.useModelButton.setEnabled(True)
            self.downloadModelButton.setEnabled(False)
            self.modelStatus = True
            print("ready")
        else:
            self.useModelButton.setEnabled(False)
            self.modelStatus = False
            print("not ready")

    def qualityOptionChanged(self, choice):
        print("Selected:", choice)
        if choice == "Select Quality":
            self.downloadModelButton.setEnabled(False)
        else:
            self.downloadModelButton.setEnabled(True)
            self.qualityChoice = choice
        self.modelCheck()

    def onPND(self):
        print("delete page nums")
        self.editor.setPlainText(removePageNums(self.editor.toPlainText()))

    def onFAD(self):
        print("delete page nums & text")
        self.editor.setPlainText(findAndDelete(self.editor.toPlainText(), self.fadEdit.toPlainText()))

    def upload_file(self):
        # getOpenFileName returns (path, selected_filter); path is "" if cancelled
        path, _ = QFileDialog.getOpenFileName(
            self, "Choose a file", "", "Text files (*.txt *.md);;All files (*)"
        )
        if not path:
            return
        try:
            text = Path(path).read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            QMessageBox.warning(self, "Could not open file", str(e))
            return
        self.editor.setPlainText(text)
        self.status.setText(f"Loaded: {Path(path).name}")
        self.fileUploadStatus = True
        self.update_buttons()
    #
    # def export_file(self):
    #     path, _ = QFileDialog.getSaveFileName(
    #         self, "Export file", "export.txt", "Text files (*.txt);;All files (*)"
    #     )
    #     if not path:
    #         return
    #     try:
    #         Path(path).write_text(self.editor.toPlainText(), encoding="utf-8")
    #     except OSError as e:
    #         QMessageBox.warning(self, "Could not save file", str(e))
    #         return
    #     QMessageBox.information(self, "Exported", f"Saved to {path}")

    def go(self, step):
        self.stack.setCurrentIndex(self.stack.currentIndex() + step)
        self.update_buttons()

    def update_buttons(self):
        index = self.stack.currentIndex()
        self.back_button.setEnabled(index > 0)
        if index >= self.stack.count() - 1:      # last page: nowhere to go
            can_go_next = False
        elif index == 0:                         # page 1: need an uploaded file
            can_go_next = self.fileUploadStatus
        elif index == 2:                         # page 3: need a model
            can_go_next = self.modelStatus
        else:                                    # page 2: free to continue
            can_go_next = True

        self.next_button.setEnabled(can_go_next)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
