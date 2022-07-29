from io import BytesIO
import base64
import pathlib

current_path = pathlib.Path(".")
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_path(stem):
    for path in current_path.rglob(stem):
        return str(path)

def get_image_info(query, conversion_dictionary):
    request_info = query.get_data().decode('UTF-8').split("|")
    image = conversion_dictionary[request_info[0][1:]]
    pallet_info = conversion_dictionary[request_info[1][0:len(request_info[1]) - 1]]
    return image, pallet_info

def get_pallet_info(query, conversion_dictionary):
    request_info = query.get_data().decode('UTF-8')
    pallet_info = conversion_dictionary[request_info[1:len(request_info) - 1]]
    return pallet_info

def get_image(img):
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    return base64.encodebytes(img_io.getvalue()).decode('ascii')

def get_pallet(img):
    img_io = BytesIO()
    img.save(img_io, 'PNG', quality=70)
    return base64.encodebytes(img_io.getvalue()).decode('ascii')
