import platform
import os

# Import Image Filter Module
if platform.system() == "Windows":
    UPLOAD_FOLDER = 'imagefilter/website/temporaryImageFiles'
    LOGFILE = "imagefilter/website/temporaryImageFileLog.txt"
else:
    UPLOAD_FOLDER = 'website/temporaryImageFiles'
    LOGFILE = "website/temporaryImageFileLog.txt"

MAX_FILE_AGE = 2

with open(LOGFILE,'r',encoding='utf-8') as logfile:
    data = logfile.readlines()

for i in range(len(data) - 1, -1, -1):
    [filename, file_age] = data[i].split(" ")
    if int(file_age) >= MAX_FILE_AGE:
        os.remove(os.path.join(UPLOAD_FOLDER, filename))
        data.pop(i)
    else:
        data[i] = filename + " " + str(int(file_age) + 1) + "\n"

with open(LOGFILE, 'w', encoding='utf-8') as logfile:
    logfile.writelines(data)