# Tanay Bennur 12/21/2021
# This module stylizes and pixelizes images with numpy and PIL

import numpy as np
import ctypes
import platform
import pathlib
from PIL import Image, ImageColor

# Import C-based stylization function, setup formatting
file_path = pathlib.Path("..")

def get_file_type():
    if platform.system() == "Windows":
        return ".dll"
    return ".so"

def get_file_path(stem):
    for path in file_path.rglob(stem):
        return str(path)

stylize = ctypes.CDLL(get_file_path("website/stylizer/stylize" + get_file_type())).stylize
stylize.restype = None
stylize.argtypes = [np.ctypeslib.ndpointer(ctypes.c_int16),
                    np.ctypeslib.ndpointer(ctypes.c_int16), 
                    ctypes.c_int, ctypes.c_int, ctypes.c_int,
                    ctypes.c_bool]

VALID_IMAGE_FORMATS = [".jpg", ".png"]
VALID_PALLET_FORMATS = [".hex"]

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

# Main stylization function, called from Flask
def convert_image(image_name, pallet_name, num_colors):
 
    data, dimensions = get_image(image_name)
    pallet = get_pallet(pallet_name, num_colors)
    stylize(data, pallet, dimensions[0], dimensions[1], num_colors, image_name.endswith(".jpg"))
        
    return Image.fromarray(np.uint8(data), 'RGB')

def visualize_pallet(pallet_name, num_colors):
    pallet = get_pallet(pallet_name, num_colors)
    
    width = int(np.ceil(num_colors**0.5))
    height = int(np.ceil(num_colors / width))
    margin = height * width - num_colors
    
    image_array = np.zeros((2 * height, 2 * width, 4), dtype="uint8")

    for i in range(2 * height):
        for j in range(2 * width):
            if i < 2 * height - 2:
                image_array[i][j][0] = pallet[width * int(i / 2) + int(j / 2)][0]
                image_array[i][j][1] = pallet[width * int(i / 2) + int(j / 2)][1]
                image_array[i][j][2] = pallet[width * int(i / 2) + int(j / 2)][2]
                image_array[i][j][3] = 255
            else:
                if j < margin or j >= 2 * width - margin:
                    continue
                else:
                    image_array[i][j][0] = pallet[width * (height - 1) + int((j - margin) / 2)][0]
                    image_array[i][j][1] = pallet[width * (height - 1) + int((j - margin) / 2)][1]
                    image_array[i][j][2] = pallet[width * (height - 1) + int((j - margin) / 2)][2]
                    image_array[i][j][3] = 255
                        
    return Image.fromarray(np.uint8(image_array), 'RGBA').resize((200, 200), resample=Image.BOX)