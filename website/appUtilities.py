from io import BytesIO
import base64
import pathlib
import os
import re
from werkzeug.utils import secure_filename

current_path = pathlib.Path(".")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_path(stem):
    for path in current_path.rglob(stem):
        return str(path)

def get_logfile_name(system):
    root_folder = ''
    if system != "Windows":
        root_folder == "website/"
    return root_folder + "temporaryImageFileLog.txt"

def edit_logfile(filename, session_id, logfile_name, replacement_necessary):
    with open(logfile_name,'r',encoding='utf-8') as logfile:
        data = logfile.readlines()
    if replacement_necessary:
        for i in range(len(data)):
            if data[i].startswith(str(session_id)):
                data[i] = ""
    with open(logfile_name, 'w', encoding='utf-8') as logfile:
        logfile.writelines(data)
    logfile = open(logfile_name, "a")
    logfile.write(filename + " 0\n")
    logfile.close()


def upload_file(filename, upload_folder, session_id, system):
    replacement_necessary = False
    for old_file in os.listdir(upload_folder):
        if old_file.startswith(str(session_id)):
            os.remove(os.path.join(upload_folder, old_file))
            replacement_necessary = True
    filepath = os.path.join(upload_folder, filename)
    edit_logfile(filename, session_id, get_logfile_name(system), replacement_necessary)
    return filepath

        

def get_image_info(query, conversion_dictionary):
    request_info = query.get_data().decode('UTF-8').split("|")
    image_name = request_info[0][1:]
    is_custom = (request_info[2][:-1] == "true")
    if is_custom:
        image = secure_filename(image_name)
    else:
        image = conversion_dictionary[image_name]
    palette_info = conversion_dictionary[request_info[1]]
    return image, palette_info, is_custom

def get_palette_info(query, conversion_dictionary):
    request_info = query.get_data().decode('UTF-8')
    palette_info = conversion_dictionary[request_info[1:len(request_info) - 1]]
    return palette_info

def get_image(img):
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    return base64.encodebytes(img_io.getvalue()).decode('ascii')

def get_palette(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG', quality=70)
    return base64.encodebytes(img_io.getvalue()).decode('ascii')
