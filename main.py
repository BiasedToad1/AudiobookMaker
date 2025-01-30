import os
import sys
import time

lim = 4000  # char limit
fcount = 1
multfiles = False

def removePageNums():
    tempLine = ""
    with open("INPUT_TEXT.txt", "r") as file:
        tempLine = file.read()
    with open("INPUT_TEXT.txt", "w") as file:
        pgs = 0
        try:
            for i in range(0, len(tempLine) - 2):
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

    with open("INPUT_TEXT.txt", "r") as inputText:
        count = 0
        file = 1
        extraLine = ""

        while True:
            # creates files
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
        global fcount
        global multfiles
        fcount = int(file)
        if file > 1:
            multfiles = True

model = ""

print("\n --- AUDIOBOOK MAKER --- \n      by BiasedToad\n    written in Python\n\nCopy Text into 'INPUT_TEXT.txt'")
confirmation = input("Enter [Y] when ready: ")
while not (confirmation == 'y' or confirmation == 'Y'):
        confirmation = input("Enter [Y] when ready: ")
confirmation = input("Delete Page Numbers? [Experimental] (y/N): ")
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
while True:
    confirmation = input("Select a Voice Model [You can test out each voice in the 'Models/' directory]\n(a/d/hf/hm/k/custom): ")
    if confirmation == 'a':
        model = "en_US-amy-medium"
        break
    elif confirmation == 'd':
        model = "en_US-danny-low"
        break
    elif confirmation == 'hf':
        model = "en_US-hfc_female-medium"
        break
    elif confirmation == 'hm':
        model = "en_US-hfc_male-medium"
        break
    elif confirmation == 'k':
        model = "en_US-kristin-medium"
        break
    elif confirmation == 'custom':
        usrmodel = input("Enter the name of the Model in the 'Models/' folder (ex: en_US-hfc_female-medium): ")
        if os.path.isfile(f"Models/{usrmodel}.onnx"):
            if os.path.isfile(f"Models/{usrmodel}.onnx.json"):
                model = usrmodel
                print(f"Using custom user model: {usrmodel}")
                break
            else:
                print("Missing .json file")
        else:
            print("Not a valid .ONNX file")
    elif os.path.isfile(f"Models/{confirmation}.onnx") and os.path.isfile(f"Models/{confirmation}.onnx.json"):
        model = confirmation
        print(f"Using custom user model: {confirmation}")
        break
    else:
        print("Not a Valid Model")

ncv = ""
if(multfiles):
    confirmation = input("Rename audio files? (y/N): ")
    if (confirmation == 'y' or confirmation == 'Y'):
        while True:
            ncv = input("Input Naming Conventions [# will be replaced with ascending numbers]\n(ex: v03c02_#): ")
            badfilename = False
            pdsn = False
            for x in ncv:
                if x == '#':
                    if pdsn == True:
                        print("Can't use more than one '#'")
                        badfilename = True
                    pdsn = True
                if x == '\\':
                    badfilename = True
            if badfilename == True or pdsn == False:
                print("Invalid File Name")
            else:
                break

zeros = False
if (not ncv == "") and (fcount >= 10):
    confirmation = input("Put 0s before lower digit numbers? [1, 2... --> 01, 02...] (y/N): ")
    if (confirmation == 'y' or confirmation == 'Y'):
        zeros = True

start = time.perf_counter()

if sys.platform == "win32":
    for i in range(1, int(fcount + 1)):
        os.system("type " + str(i) + ".txt | .\\piperw\\piper.exe -m Models/" + model + ".onnx -f " + str(i) + ".wav")
        os.system("erase " + str(i) + ".txt")
        if ncv == "":
            os.system("move " + str(i) + ".wav completed/")
        else:
            if zeros == True:
                if fcount < 100:
                    if i < 10:
                        tempstr = "0" + str(i)
                        os.system("move " + str(i) + ".wav completed/" + ncv.replace("#", tempstr) + ".wav")
                    else:
                        os.system("move " + str(i) + ".wav completed/" + ncv.replace("#", str(i)) + ".wav")
                if fcount < 1000:
                    if i < 100 and i >= 10:
                        tempstr = "0" + str(i)
                        os.system("move " + str(i) + ".wav completed/" + ncv.replace("#", tempstr) + ".wav")
                    elif i < 10:
                        tempstr = "00" + str(i)
                        os.system("move " + str(i) + ".wav completed/" + ncv.replace("#", tempstr) + ".wav")
                    else:
                        os.system("move " + str(i) + ".wav completed/" + ncv.replace("#", str(i)) + ".wav")

            if zeros == False:
                os.system("move " + str(i) + ".wav completed/" + ncv.replace("#", str(i)) + ".wav")

elif sys.platform == "linux":
    for i in range(1, int(fcount + 1)):
        os.system("cat " + str(i) + ".txt | ./piper/piper -m Models/" + model + ".onnx -f " + str(i) + ".wav")
        os.system("ffmpeg -i " + str(i) + ".wav " + str(i) + ".mp3")
        o = str(i) + ".txt"
        try:
            os.remove(o)
        except FileNotFoundError:
            pass
        o = str(i) + ".wav"
        try:
            os.remove(o)
        except FileNotFoundError:
            pass
        if ncv == "":
            os.system("mv " + str(i) + ".mp3 completed/")
        else:
            if zeros == True:
                if fcount < 100:
                    if i < 10:
                        tempstr = "0" + str(i)
                        os.system("mv " + str(i) + ".mp3 completed/" + ncv.replace("#", tempstr) + ".mp3")
                    else:
                        os.system("mv " + str(i) + ".mp3 completed/" + ncv.replace("#", str(i)) + ".mp3")
                if fcount < 1000:
                    if i < 100 and i >= 10:
                        tempstr = "0" + str(i)
                        os.system("mv " + str(i) + ".mp3 completed/" + ncv.replace("#", tempstr) + ".mp3")
                    elif i < 10:
                        tempstr = "00" + str(i)
                        os.system("mv " + str(i) + ".mp3 completed/" + ncv.replace("#", tempstr) + ".mp3")
                    else:
                        os.system("mv " + str(i) + ".mp3 completed/" + ncv.replace("#", str(i)) + ".mp3")

            if zeros == False:
                os.system("mv " + str(i) + ".mp3 completed/" + ncv.replace("#", str(i)) + ".mp3")

end = time.perf_counter()
time = int(end - start)
secs = time % 60
mins = int(time / 60) % 60
hours = int((time / 60) / 60) % 60

print(f"\nProgram complete in {hours:02}:{mins:02}:{secs:02}, New audiobook files moved to ./completed/\n")
