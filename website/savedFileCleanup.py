import platform
import os
import pathlib

current_path = pathlib.Path("..")

def get_file_path(stem):
    for path in current_path.rglob(stem):
        return str(path)

UPLOAD_FOLDER = get_file_path("temporaryImageFiles")
LOGFILE = get_file_path("temporaryImageFileLog.txt")

MAX_FILE_AGE = 2

with open(LOGFILE,'r',encoding='utf-8') as logfile:
    data = logfile.readlines()

for i in range(len(data) - 1, -1, -1):
    [filename, file_age] = data[i].split(" ")
    if int(file_age) >= MAX_FILE_AGE:
        data.pop(i)
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, filename))
        except:
            pass
    else:
        data[i] = filename + " " + str(int(file_age) + 1) + "\n"

with open(LOGFILE, 'w', encoding='utf-8') as logfile:
    logfile.writelines(data)
