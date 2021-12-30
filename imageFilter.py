# Tanay Bennur 12/21/2021
# Stylizes and Pixelizes Images with numpy and PIL
# Find palettes at https://lospec.com/palette-list and download as hex file


import time
import numpy as np
import ctypes
from PIL import Image, ImageColor


stylize = ctypes.CDLL("../imageFilter/stylize.dll").stylize
stylize.restype = None
stylize.argtypes = [np.ctypeslib.ndpointer(ctypes.c_int16),
                    np.ctypeslib.ndpointer(ctypes.c_int16), 
                    ctypes.c_int, ctypes.c_int, ctypes.c_int,
                    ctypes.c_bool]


VALID_IMAGE_FORMATS = [".jpg", ".png"]
VALID_PALLET_FORMATS = [".hex"]

def is_valid_image(image_name):
    for format in VALID_IMAGE_FORMATS:
        if image_name.endswith(format): return True
    return False

def is_valid_pallet(pallet_name):
    for format in VALID_PALLET_FORMATS:
        if pallet_name.endswith(format): return True
    return False

def print_timings(dimensions, num_colors, timings):
    
    print("\nPARAMETERS")
    print("Image Size: ", dimensions[0], " by ", dimensions[1])
    print("Pallet Size: ", num_colors)
    
    print("\nTIMINGS")
    print("Setup: " , timings[1] - timings[0])
    print("Stylization: " , timings[2] - timings[1], "\n")


def get_image(image_name):
    
    if (not is_valid_image(image_name)): raise Exception("Invalid Image Format")

    try:
        img = Image.open("Images/" + image_name)
    except FileNotFoundError:
        raise Exception("Non-Existent Image File")
    
    img.load()
    data = np.asarray(img, dtype = "int16")[:, :, 0:3]
    dimensions = [len(data), len(data[0])]

    return data, dimensions

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
        colorList = open("Palettes/" + pallet_folder(num_colors) + pallet_name)
    except FileNotFoundError:
        raise Exception("Non-Existent Pallet File")
    
    palletList = []
    
    for color in colorList:
        palletList.append(ImageColor.getcolor("#" + color, "RGB"))
    
    if len(palletList) != num_colors:
        raise Exception("Incorrect Pallet Size")
    
    return convert_pallet(palletList)


def convertImage(image_name, pallet_name, num_colors, should_time = False):

    t0 = time.time()

    data, dimensions = get_image(image_name)
    pallet = get_pallet(pallet_name, num_colors)
    
    t1 = time.time()
    
    stylize(data, pallet, dimensions[0], dimensions[1], num_colors, image_name.endswith(".jpg"))
    
    t2 = time.time()
        
    img = Image.fromarray(np.uint8(data), 'RGB')
    img.show()
    
    if should_time: print_timings(dimensions, num_colors, [t0, t1, t2])

convertImage(image_name = "pittsburgh.jpg", pallet_name = "fantasy-32.hex", num_colors = 32, should_time = True)