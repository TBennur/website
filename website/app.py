from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
import yaml
import platform
import uuid
from werkzeug import utils, exceptions
from datetime import timedelta
import base64

# Import Modules
if platform.system() == "Windows":
    import widgets.imageFilter as stylizerWidget
    import widgets.cipherGame as cipherWidget
    import appUtilities
else:
    from website.widgets import imageFilter as stylizerWidget
    from website.widgets import cipherGame as cipherWidget
    from website import appUtilities

# Setup webpage and import constants
app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes = 30)
app.config['UPLOAD_FOLDER'] = appUtilities.get_file_path('temporaryImageFiles')
app.config['MAX_CONTENT_LENGTH'] = 500 * 1000
Session(app)

conversion_stream = open(appUtilities.get_file_path("widgets/stylizeNameConversion.yaml"), 'r')
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
    image, palette_info, is_custom = appUtilities.get_image_info(request, conversion_dictionary)
    try:
        img = stylizerWidget.convert_image(image, palette_info['filename'], palette_info['size'], is_custom, session["id"])    
        encoded_img = appUtilities.get_image(img)
        return jsonify({ 'Status' : 'Success', 'ImageBytes': encoded_img})
    except AttributeError:
        return jsonify({'Status' : 'Failure', 'Reason' : 'You recently uploaded a different file. Due to space constraints, only 1 user file can be processed at a time. Please reupload this file.'})

# Visualizes current palette
@app.route('/visualize-palette', methods = ["GET", "POST"])
def visualize_palette():
    palette_info = appUtilities.get_palette_info(request, conversion_dictionary)
    img = stylizerWidget.visualize_palette(palette_info['filename'], palette_info['size'])
    encoded_img = appUtilities.get_palette(img)
    return jsonify({ 'Status' : 'Success', 'ImageBytes': encoded_img})

# Cipher Game route
@app.route("/cipher")
def cipher():
    session["raw_text"], session["cipher_rules"], session["cipher_text"], session["user_rules"], session["user_hints"], session["user_text"] = cipherWidget.reset_decoder()
    return render_template("cipher.html")

# Hint button for cipher game
@app.route('/hint-button', methods = ["GET", "POST"])
def hint_button():
    cipherWidget.update_hints(session["user_hints"], session["user_rules"], session["cipher_rules"])
    session["user_text"] = cipherWidget.replace_text(session["cipher_text"], session["user_rules"] + session["user_hints"])
    return jsonify({ 'Status' : 'Success', 
                    'text': session["user_text"], 
                    'rules': cipherWidget.format_rules(session["user_rules"]),
                    'hints': cipherWidget.format_hints(session["user_hints"]), 
                    'raw': session["cipher_text"],
                    'win': str(session["user_text"] == session["raw_text"])})

# Replacement button for cipher game
@app.route('/replace-button', methods = ["GET", "POST"])
def replace_button():
    [l1, l2] = request.get_data().decode('UTF-8').split("|")
    cipherWidget.update_rules(l1, l2, session["user_rules"], session["user_hints"])
    session["user_text"] = cipherWidget.replace_text(session["cipher_text"], session["user_rules"] + session["user_hints"])
    return jsonify({ 'Status' : 'Success', 
                    'text': session["user_text"], 
                    'rules': cipherWidget.format_rules(session["user_rules"]),
                    'hints': cipherWidget.format_hints(session["user_hints"]), 
                    'raw': session["cipher_text"],
                    'win': str(session["user_text"] == session["raw_text"])})

# Visualizes Uploaded Image
@app.route('/visualize-image', methods = ["GET", "POST"])
def visualize_image():
    if 'file' not in request.files:
        return jsonify({'Status' : 'Failure', 'Reason' : 'File Doesn\'t Exist'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'Status' : 'Failure', 'Reason' : 'Please Upload a Named File'})
    if file and appUtilities.allowed_file(file.filename):
        filename = str(session["id"]) + "-file-" + utils.secure_filename(file.filename)
        filepath = appUtilities.upload_file(filename, app.config["UPLOAD_FOLDER"], session["id"], platform.system())
        file.save(filepath)
        return jsonify({ 'Status' : 'Success', 'ImageBytes': base64.encodebytes(file.getvalue()).decode('ascii')})
    return jsonify({'Status' : 'Failure', 'Reason' : 'Please Upload a JPEG or PNG'})

@app.errorhandler(exceptions.RequestEntityTooLarge)
def handle_bad_request(e):
    return jsonify({'Status' : 'Failure', 'Reason' : 'Please Upload a File Smaller than 500 KB'})

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