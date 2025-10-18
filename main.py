import os
import sys
import time
import wave
from piper import PiperVoice

model = ""
lim = 4000  # char limit
fileCount = 1
multipleFiles = False 

def removePageNums():
    tempLine = ""
    with open("INPUT_TEXT.txt", "r") as file: # opens the file and copies all text onto tempLine
        tempLine = file.read()
    with open("INPUT_TEXT.txt", "w") as file:
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
        finally:
            file.write(tempLine)
            print(f"Page Numbers Deleted: {pgs}")

def textDivider():
    count = 0
    removePgNums = None
    line = ""

    # deletes previous files
    while count < 999:
        o = str(count) + ".txt"
        try:
            os.remove(o)
        except FileNotFoundError:
            pass
        finally:
            count += 1
    print("files deleted")

    # creates files
    with open("INPUT_TEXT.txt", "r") as inputText:
        count = 0
        file = 1
        extraLine = ""

        while True:
            o = str(file) + ".txt"
            with open(o, "w") as outputText:
                outputText.write(extraLine)
                count += (len(extraLine) + 1)

                for line in inputText:
                    count += (len(line) + 1)
                    if count > lim:
                        count = 0;
                        extraLine = line + " "
                        break
                    outputText.write(line + " ")

            if count == 0:
                file += 1
            else:
                break

        print(f"Created {file} files")
        global fileCount
        global multipleFiles
        fileCount = int(file)
        if file > 1:
            multipleFiles = True

def renamerZeros(files, num, zeros): # used to determine if and how many zeros should go before number
    if zeros == False:
        return num
    if files < 100:
        if num < 10:
            tempstr = "0" + str(num)
            return tempstr
        else:
            return num
    if files < 1000 and num < 100 and num >= 10:
        tempstr = "0" + str(num)
        return tempstr
    elif files < 1000 and num < 10:
        tempstr = "00" + str(num)
        return tempstr
    else:
        return num

def modelDownloader():
    voices = {"amy","arctic","bryce","danny","hfc_female","hfc_male","joe","john","kathleen","kristin","kusal","l2arctic","lessac","libritts","ljspeech","norman","reza_ibrahim","ryan","sam"}
    while True:
        modelChoice = input(f"Choose a voice model to download\n{voices}\n:")
        if modelChoice in voices:
            while True:
                qualityChoice = input("Select a quality option [low/medium/high]\n:")
                if qualityChoice == "low" or qualityChoice == "medium" or qualityChoice == "high":
                    os.system(f"python3 -m piper.download_voices en_US-{modelChoice}-{qualityChoice}")
                    if(os.path.exists(f"en_US-{modelChoice}-{qualityChoice}.onnx")):
                        os.rename(f"en_US-{modelChoice}-{qualityChoice}.onnx", f"models/en_US-{modelChoice}-{qualityChoice}.onnx")
                        os.rename(f"en_US-{modelChoice}-{qualityChoice}.onnx.json", f"models/en_US-{modelChoice}-{qualityChoice}.onnx.json")
                        break
                    else:
                        print("Failed to download, quality option not available")
                else:
                    print("Quality option not available")
            break

def modelIndex():
    lst = os.listdir("models/")
    if not lst:
        return 0
    for x in lst:
        if not x.endswith(".onnx"):
            lst.remove(x)
    for x in range(len(lst)):
        lst[x] = lst[x].replace("en_US-", "")
        lst[x] = lst[x].replace(".onnx", "")
    for x in lst:
        if x.endswith(".json"):
            lst.remove(x)
    return lst

def modelChooser():
    global model
    while modelIndex() == 0:
        print("You currently have no models downloaded")
        modelDownloader()

    
    print(f"{modelIndex()} voice models detected.\nEnter model name to use or enter \'DOWNLOAD\' to download a new model.")
    while True:
        choice = input(":")
        try:
            if choice in modelIndex():
                model = f"en_US-{choice}"
                break
            elif choice == "DOWNLOAD":
                modelDownloader()
                print(f"{modelIndex()} voice models detected.\nEnter model name to use or enter \'DOWNLOAD\' to download a new model.")
                continue
            else:
                print("Not a valid choice.")
        except ValueError: 
            print("Not a valid choice.")

if __name__ == "__main__":
    if not (os.path.exists("multi")): os.mkdir("multi")
    if not (os.path.exists("models")): os.mkdir("models")
    if not (os.path.exists("completed")): os.mkdir("completed")

    print("\n --- AUDIOBOOK MAKER --- \n      by BiasedToad\n    written in Python\n\n")

    choice = input("Create an Audiobook [1]\nSplit Text Files    [2]\nDelete Page Numbers [3]\n:")
    while not (choice == '1' or choice == '2' or choice == '3'):
        choice = input(":")
    choice = int(choice)

    if choice == 1:
        confirmation = input("Make Multiple Books? [Experimental] (y/N): ")
        if confirmation == 'y' or confirmation == 'Y':
            choice = 4

    if choice == 1: #  Make an Audiobook

        confirmation = input("\nCopy Text into 'INPUT_TEXT.txt'\nEnter [Y] when ready: ")
        while not (confirmation == 'y' or confirmation == 'Y'):
            confirmation = input("Enter [Y] when ready: ")

        confirmation = input("Delete Page Numbers? (y/N): ")
        if (confirmation == 'y' or confirmation == 'Y'):
            removePageNums()

        confirmation = input("Split Audio Files? (y/N): ")
        if (confirmation == 'y' or confirmation == 'Y'):
            confirmation = input("Max Text Character Size? (4000 default): ")
            if confirmation.isdigit():
                lim = int(confirmation)
            textDivider()
        else:
            with open("INPUT_TEXT.txt", "r") as file:
                tempLine = file.read()
            with open("1.txt", "w") as file:
                file.write(tempLine)

        modelChooser()

        nameConvs = ""
        if(multipleFiles):
            confirmation = input("Rename audio files? (y/N): ")
            if (confirmation == 'y' or confirmation == 'Y'):
                while True:
                    nameConvs = input("Input Naming Conventions [# will be replaced with ascending numbers]\n(ex: v03c02_#): ")
                    badfilename = False
                    usedHashtag = False
                    for x in nameConvs:
                        if x == '#':
                            if usedHashtag == True:
                                print("Can't use more than one '#'")
                                badfilename = True
                            usedHashtag = True
                        if x == '\\':
                            badfilename = True
                    if badfilename == True or usedHashtag == False:
                        print("Invalid File Name")
                    else:
                        break

        zeros = False
        if (nameConvs != "") and (fileCount >= 10):
            confirmation = input("Put 0s before lower digit numbers? [1, 2... --> 01, 02...] (y/N): ")
            if (confirmation == 'y' or confirmation == 'Y'):
                zeros = True

        start = time.perf_counter()

        for i in range(1, int(fileCount + 1)):
            o = str(i) + ".txt"
            voice = PiperVoice.load("models/" + model + ".onnx")
            with open(str(i) + ".txt", "r") as txt:
                with wave.open(str(i) + ".wav", "wb") as wav_file:
                    voice.synthesize_wav(txt.read(), wav_file)
                        
            try:
                os.remove(o)
            except FileNotFoundError:
                pass
            if nameConvs != "":
                os.rename(f"{str(i)}.wav", f"completed/{nameConvs.replace("#", str(renamerZeros(fileCount, i, zeros)))}.wav")
            else:
                os.rename(f"{str(i)}.wav", f"completed/{str(i)}.wav")

        end = time.perf_counter()
        time = int(end - start)
        secs = time % 60
        mins = int(time / 60) % 60
        hours = int((time / 60) / 60) % 60

        print(f"\nProgram complete in {hours:02}:{mins:02}:{secs:02}, New audiobook files moved to ./completed/\n")

    elif choice == 2: # Split Text Files

        confirmation = input("Max Text Character Size? (4000 default): ")
        if confirmation.isdigit():
            lim = int(confirmation)
        textDivider()

    elif choice == 3:

        removePageNums()

    elif choice == 4:

        pgNumBool = False
        splitTextBool = False


        confirmation = input("\nCopy Files into 'multi/'\nEnter [Y] when ready: ")
        while not (confirmation == 'y' or confirmation == 'Y'):
            confirmation = input("Enter [Y] when ready: ")

        confirmation = input("Use Default Audiobook Properties? (Y/n): ")
        if (confirmation == 'n' or confirmation == 'N'):

            confirmation = input("Delete Page Numbers? (y/N): ")
            if (confirmation == 'y' or confirmation == 'Y'):
                pgNumBool = True

            confirmation = input("Split Audio Files? (y/N): ")
            if (confirmation == 'y' or confirmation == 'Y'):
                confirmation = input("Max Text Character Size? (4000 default): ")
                if confirmation.isdigit():
                    lim = int(confirmation)
                splitTextBool = True

        modelChooser()

        start = time.perf_counter()
        os.system("ls -1 multi/ > files.txt")
        with open('files.txt', 'r') as file:
            for line in file:
                os.system("cat multi/" + line.strip() + " > INPUT_TEXT.txt")
                if pgNumBool == True:
                    removePageNums()
                if splitTextBool == True:
                    textDivider()
                else:
                    os.system("cat INPUT_TEXT.txt > 1.txt")

                os.mkdir("completed/" + line.strip())
                for i in range(1, int(fileCount + 1)):
                    voice = PiperVoice.load("models/" + model + ".onnx")
                    with open(str(i) + ".txt", "r") as txt:
                        with wave.open("completed/" + line.strip() + "/" + str(i) + ".wav", "wb") as wav_file:
                            voice.synthesize_wav(txt.read(), wav_file)
                    o = str(i) + ".txt"
                    try:
                        os.remove(o)
                    except FileNotFoundError:
                        pass

        os.remove("files.txt")

        end = time.perf_counter()
        time = int(end - start)
        secs = time % 60
        mins = int(time / 60) % 60
        hours = int((time / 60) / 60) % 60

        print(f"\nProgram complete in {hours:02}:{mins:02}:{secs:02}, New audiobooks moved to ./completed/\n")