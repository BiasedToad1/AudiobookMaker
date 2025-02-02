# Choose a Model from the 'Models/' folder

model = "en_US-hfc_male-medium"

# Delete page numbers? [True/False]

deletePageNumbers = False

# Split Audio Files? [True/False]

splitAudioFiles = False

# Max Text Character Size, only use if splitAudioFiles is True

maxTextCharacterSize = 4000

# Rename audio files [True/False], only use if splitAudioFiles is True

renameAudioFiles = False

# Input Naming Conventions, only use if renameAudioFiles is True

namingConventions = ""

# Put 0s before lower digit numbers? [True/False]

zeroesLowerDigits = False







from main.py import removePageNums, textDivider, renamerZeros
import subprocess

subprocess.run(["ollama", "run", "deepseek-r1:1.5b", "PROMT=\"summarize this: " + tempLine + "\""], capture_output=True)
