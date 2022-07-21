import pathlib
import platform
import numpy as np
from PIL import Image, ImageColor


file_path = pathlib.Path("..")

VALID_IMAGE_FORMATS = [".jpg", ".png"]
VALID_PALLET_FORMATS = [".hex"]

def get_file_type():
    if platform.system() == "Windows":
        return ".dll"
    return ".so"

def get_file_path(stem):
    for path in file_path.rglob(stem):
        return str(path)

# Check parameter validity for pallets and images
def is_valid_image(image_name):
    for format in VALID_IMAGE_FORMATS:
        if image_name.endswith(format): return True
    return False

def is_valid_pallet(pallet_name):
    for format in VALID_PALLET_FORMATS:
        if pallet_name.endswith(format): return True
    return False

# Retrieve and setup/load pallets and images
def pallet_folder(num_colors):
    if num_colors < 0:
        raise Exception("Invalid Number of Colors")
    elif num_colors < 8:
        return "palletSmall/"
    elif num_colors == 8:
        return "pallet8/"
    elif num_colors == 16:
        return "pallet16/"
    elif num_colors == 32:
        return "pallet32/"
    elif num_colors > 32:
        return "palletLarge/"
    return "palletCustom/"

def convert_pallet(pallet_list):
    pallet = np.zeros((len(pallet_list), 3), dtype = "int16")
    for x in range(len(pallet_list)):
        pallet[x][0] = pallet_list[x][0]
        pallet[x][1] = pallet_list[x][1]
        pallet[x][2] = pallet_list[x][2]
    return pallet

def get_pallet(pallet_name, num_colors):
    if (not is_valid_pallet(pallet_name)): raise Exception("Invalid Pallet Format")
    if pallet_name == "temp_results.hex":
        colorList = open(get_file_path("../static/defaultFiles/Palettes/palletCustom/" + pallet_name))        
    else:
        try:
            colorList = open(get_file_path("../static/defaultFiles/Palettes/" + pallet_folder(num_colors) + pallet_name))
        except FileNotFoundError:
            raise Exception("Non-Existent Pallet File")
    
    palletList = []
    for color in colorList:
        palletList.append(ImageColor.getcolor("#" + color, "RGB"))
    if len(palletList) != num_colors:
        raise Exception("Incorrect Pallet Size")
    return convert_pallet(palletList)

def get_image(image_name):
    if (not is_valid_image(image_name)): raise Exception("Invalid Image Format")
    try:
        img = Image.open(get_file_path("../static/defaultFiles/Images/" + image_name))
    except FileNotFoundError:
        raise Exception("Non-Existent Image File")
    
    img.load()
    data = np.asarray(img, dtype = "int16")[:, :, 0:3]
    dimensions = [len(data), len(data[0])]
    return data, dimensions