from flask import Flask, render_template, request, jsonify, session, url_for
from flask_session import Session
import yaml
import platform
import uuid
import os
from werkzeug import utils, exceptions
from datetime import timedelta
import base64

# Import Image Filter Module
if platform.system() == "Windows":
    import stylizer.imageFilter as imageFilter
    import appUtilities
else:
    from website.stylizer import imageFilter
    from website import appUtilities

# Setup webpage and import constants
UPLOAD_FOLDER = 'temporaryImageFiles'
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 30)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 5 * 1000 * 1000
Session(app)

conversion_stream = open(appUtilities.get_file_path("stylizer/stylizeNameConversion.yaml"), 'r')
conversion_dictionary = yaml.safe_load(conversion_stream)

# Homepage route
@app.route("/")
def home():
    return render_template("home.html")

# Stylizer Route    
@app.route("/stylizer")
def stylizer():
    session["id"] = uuid.uuid4()
    return render_template("stylizer.html")

# Main stylization function, creates and converts stylized image
@app.route('/stylize-button', methods = ["GET", "POST"])
def stylize_button():
    image, pallet_info = appUtilities.get_image_info(request, conversion_dictionary)
    img = imageFilter.convert_image(image, pallet_info['filename'], pallet_info['size'])    
    encoded_img = appUtilities.get_image(img)
    return jsonify({ 'Status' : 'Success', 'ImageBytes': encoded_img})

# Visualizes Current Pallet
@app.route('/visualize-palette', methods = ["GET", "POST"])
def visualize_palette():
    pallet_info = appUtilities.get_pallet_info(request, conversion_dictionary)
    img = imageFilter.visualize_pallet(pallet_info['filename'],pallet_info['size'])
    encoded_img = appUtilities.get_pallet(img)
    return jsonify({ 'Status' : 'Success', 'ImageBytes': encoded_img})

# Visualizes Uploaded Image
@app.route('/visualize-image', methods = ["GET", "POST"])
def visualize_image():
    if 'file' not in request.files:
        return jsonify({'Status' : 'Failure'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'Status' : 'Failure'})
    if file and appUtilities.allowed_file(file.filename):
        filename = str(session["id"]) + "-file-" + utils.secure_filename(file.filename)
        for old_file in os.listdir(app.config["UPLOAD_FOLDER"]):
            if old_file.startswith(str(session["id"])):
                print("Old File Found")
                os.remove(os.path.join(app.config['UPLOAD_FOLDER'], old_file))
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        print(type(file))
        print("Uploaded")
        return jsonify({ 'Status' : 'Success', 'ImageBytes': base64.encodebytes(file.getvalue()).decode('ascii')})
    return jsonify({'Status' : 'Failure'})

@app.errorhandler(exceptions.RequestEntityTooLarge)
def handle_bad_request(e):
    return jsonify({'Status' : 'Failure'})

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

if __name__ == "__main__":
    app.run()