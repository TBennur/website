from flask import Flask, render_template, request, jsonify
import yaml
import platform

# Import Image Filter Module
if platform.system() == "Windows":
    import stylizer.imageFilter as imageFilter
    import appUtilities
else:
    from website.stylizer import imageFilter
    from website import appUtilities

# Setup webpage and import constants
app = Flask(__name__)

conversion_stream = open(appUtilities.get_file_path("stylizer/stylizeNameConversion.yaml"), 'r')
conversion_dictionary = yaml.safe_load(conversion_stream)

# Homepage route
@app.route("/")
def home():
    return render_template("home.html")

# Stylizer Route    
@app.route("/stylizer")
def stylizer():
    return render_template("stylizer.html")

# Main stylization function, creates and converts stylized image
@app.route('/stylize-button', methods = ["GET", "POST"])
def stylize_button():
    image, pallet_info = appUtilities.get_image_info(request, conversion_dictionary)
    img = imageFilter.convert_image(image, pallet_info['filename'], pallet_info['size'])    
    encoded_img = appUtilities.get_image(img)
    return jsonify({ 'Status' : 'Success', 'ImageBytes': encoded_img})

# Visualizes Current Pallet
@app.route('/visualize-pallet', methods = ["GET", "POST"])
def visualize_pallet():
    pallet_info = appUtilities.get_pallet_info(request, conversion_dictionary)
    img = imageFilter.visualize_pallet(pallet_info['filename'],pallet_info['size'])
    encoded_img = appUtilities.get_pallet(img)
    return jsonify({ 'Status' : 'Success', 'ImageBytes': encoded_img})

# About me page route
@app.route("/about")
def about():
    return render_template("about.html")

# Coursework page route
@app.route("/coursework")
def coursework():
    return render_template("coursework.html")

# Projects page route
@app.route("/projects")
def projects():
    return render_template("projects.html")

# Contact page route
@app.route("/contact")
def contact():
    return render_template("contact.html")

if __name__ == "__main__":
    app.run()