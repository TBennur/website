import pathlib
import platform
import numpy as np
from PIL import Image, ImageColor


file_path = pathlib.Path("..")

VALID_IMAGE_FORMATS = [".jpg", ".png", ".jpeg"]
VALID_PALETTE_FORMATS = [".hex"]

def get_file_type():
    if platform.system() == "Windows":
        return ".dll"
    return ".so"

def get_file_path(stem):
    for path in file_path.rglob(stem):
        return str(path)

# Check parameter validity for palettes and images
def is_valid_image(image_name):
    for format in VALID_IMAGE_FORMATS:
        if image_name.endswith(format): return True
    return False

def is_valid_palette(palette_name):
    for format in VALID_PALETTE_FORMATS:
        if palette_name.endswith(format): return True
    return False

# Retrieve and setup/load palettes and images
def palette_folder(num_colors):
    if num_colors < 0:
        raise Exception("Invalid Number of Colors")
    elif num_colors < 8:
        return "paletteSmall/"
    elif num_colors == 8:
        return "palette8/"
    elif num_colors == 16:
        return "palette16/"
    elif num_colors == 32:
        return "palette32/"
    elif num_colors > 32:
        return "paletteLarge/"
    return "paletteCustom/"

def convert_palette(palette_list):
    palette = np.zeros((len(palette_list), 3), dtype = "int16")
    for x in range(len(palette_list)):
        palette[x][0] = palette_list[x][0]
        palette[x][1] = palette_list[x][1]
        palette[x][2] = palette_list[x][2]
    return palette

def get_palette(palette_name, num_colors):
    if (not is_valid_palette(palette_name)): raise Exception("Invalid palette Format")
    if palette_name == "temp_results.hex":
        colorList = open(get_file_path("*/Palettes/paletteCustom/" + palette_name))        
    else:
        try:
            colorList = open(get_file_path("*/Palettes/" + palette_folder(num_colors) + palette_name))
        except FileNotFoundError:
            raise Exception("Non-Existent palette File")
    
    paletteList = []
    for color in colorList:
        paletteList.append(ImageColor.getcolor("#" + color, "RGB"))
    if len(paletteList) != num_colors:
        raise Exception("Incorrect palette Size")
    return convert_palette(paletteList)

def get_image(image_name, is_custom, session_id):
    if (not is_valid_image(image_name)): raise Exception("Invalid Image Format")
    if is_custom:
        try:
            img = Image.open(get_file_path(str(session_id) + "-file-" + image_name))
        except FileNotFoundError:
            raise Exception("Non-Existent Image File")
    else:
        try:
            img = Image.open(get_file_path("*/Images/" + image_name))
        except FileNotFoundError:
            raise Exception("Non-Existent Image File")
    
    img.load()
    data = np.asarray(img, dtype = "int16")[:, :, 0:3]
    dimensions = [len(data), len(data[0])]
    return data, dimensions