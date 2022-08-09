# Tanay Bennur 12/21/2021
# This module stylizes and pixelizes images with numpy and PIL

import numpy as np
import ctypes
from PIL import Image
import platform

if platform.system() == "Windows":
    import stylizer.filterUtilities as filterUtilities
else:
    import website.stylizer.filterUtilities as filterUtilities

# Import C-based stylization function, setup formatting
stylize = ctypes.CDLL(filterUtilities.get_file_path("website/stylizer/stylize" + filterUtilities.get_file_type())).stylize
stylize.restype = None
stylize.argtypes = [np.ctypeslib.ndpointer(ctypes.c_int16),
                    np.ctypeslib.ndpointer(ctypes.c_int16), 
                    ctypes.c_int, ctypes.c_int, ctypes.c_int,
                    ctypes.c_bool]

# Main stylization function, called from Flask
def convert_image(image_name, palette_name, num_colors, is_custom, session_id):
    data, dimensions = filterUtilities.get_image(image_name, is_custom, session_id)
    palette = filterUtilities.get_palette(palette_name, num_colors)
    stylize(data, palette, dimensions[0], dimensions[1], num_colors, image_name.endswith(".jpg"))
    return Image.fromarray(np.uint8(data), 'RGB')

def visualize_palette(palette_name, num_colors):
    
    palette = filterUtilities.get_palette(palette_name, num_colors)
    
    width = int(np.ceil(num_colors**0.5))
    height = int(np.ceil(num_colors / width))
    margin = height * width - num_colors
    image_array = np.zeros((2 * height, 2 * width, 4), dtype="uint8")

    for i in range(2 * height):
        for j in range(2 * width):
            if i < 2 * height - 2:
                image_array[i][j][0] = palette[width * int(i / 2) + int(j / 2)][0]
                image_array[i][j][1] = palette[width * int(i / 2) + int(j / 2)][1]
                image_array[i][j][2] = palette[width * int(i / 2) + int(j / 2)][2]
                image_array[i][j][3] = 255
            else:
                if j < margin or j >= 2 * width - margin:
                    continue
                else:
                    image_array[i][j][0] = palette[width * (height - 1) + int((j - margin) / 2)][0]
                    image_array[i][j][1] = palette[width * (height - 1) + int((j - margin) / 2)][1]
                    image_array[i][j][2] = palette[width * (height - 1) + int((j - margin) / 2)][2]
                    image_array[i][j][3] = 255
                        
    return Image.fromarray(np.uint8(image_array), 'RGBA').resize((200, 200), resample=Image.BOX)
