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

conversion_stream = open(appUtilities.get_file_path("stylizeNameConversion.yaml"), 'r')
conversion_dictionary = yaml.safe_load(conversion_stream)

# Homepage route
@app.route("/")
def home():
    return render_template("home.html")

# Stylizer Route    
@app.route("/stylizer", methods = ["GET", "POST"])
def stylizer():
    if request.method == 'POST':
        if "palette-primary" in request.form:
            session["stylizer"]["primary_palette"] = request.form["palette-primary"]
            if "palette-secondary" in request.form:
                session["stylizer"]["secondary_palette"] = request.form["palette-secondary"]
                if request.form["palette-primary"] != "Please Select a Palette Size" and request.form["palette-secondary"] != "Please Select a Palette":
                    palette_info = conversion_dictionary[request.form["palette-secondary"]]
                    img = stylizerWidget.visualize_palette(palette_info["filename"], palette_info["size"])
                    session["stylizer"]["palette_image"] = "data:image/png;base64," + appUtilities.get_palette(img)
    else:
        session["id"] = uuid.uuid4()
        session["stylizer"] = {"primary_palette": "Please Select a Palette Size",
                               "secondary_palette": "Please Select a Palette",
                               "palette_image": "data:image/png;base64,"}
   
    context = {"primary_palettes": ["Please Select a Palette Size", "Small", "8-Color", "16-Color", "32-Color", "Large"],
               "primary_selected": session["stylizer"]["primary_palette"] != "Please Select a Palette Size",
               "primary_palette": session["stylizer"]["primary_palette"],
               "secondary_palettes": conversion_dictionary[session["stylizer"]["primary_palette"]],
               "secondary_selected": session["stylizer"]["primary_palette"] != "Please Select a Palette Size" and session["stylizer"]["secondary_palette"] != "Please Select a Palette",
               "secondary_palette": session["stylizer"]["secondary_palette"],
               "palette_image": session["stylizer"]["palette_image"]}
    
    return render_template("stylizer.html", **context)

# Main stylization function, creates and converts stylized image
@app.route('/stylize-button', methods = ["GET", "POST"])
def stylize_button():
    image, is_custom = appUtilities.get_image_info(request, conversion_dictionary)
    palette_info = conversion_dictionary[session["stylizer"]["secondary_palette"]]
    try:
        img = stylizerWidget.convert_image(image, palette_info['filename'], palette_info['size'], is_custom, session["id"])    
        encoded_img = appUtilities.get_image(img)
        return jsonify({ 'Status' : 'Success', 'ImageBytes': encoded_img})
    except AttributeError:
        return jsonify({'Status' : 'Failure', 'Reason' : 'You recently uploaded a different file. Due to space constraints, only 1 user file can be processed at a time. Please reupload this file.'})

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

# Cipher Game
@app.route("/cipher", methods = ["GET", "POST"])
def cipher():
    
    if request.method == 'POST':
        if "hint" in request.form:
            cipher_data = session["cipher"]
            cipherWidget.update_hints(cipher_data["user_hints"], cipher_data["user_rules"], cipher_data["cipher_rules"])
        elif "replace" in request.form:
            cipher_data = session["cipher"]
            cipherWidget.update_rules(cipher_data["old_letter"], cipher_data["new_letter"], cipher_data["user_rules"], cipher_data["user_hints"])
        elif "old_letter" in request.form:
            session["cipher"]["old_letter"] = request.form["old_letter"]
        elif "new_letter" in request.form:
            session["cipher"]["new_letter"] = request.form["new_letter"]
        else:
            session["cipher"] = cipherWidget.setup()
    else:
        session["cipher"] = cipherWidget.setup()
    
    cipher_data = session["cipher"]
    session["cipher"]["user_text"] = cipherWidget.replace_text(cipher_data["cipher_text"], cipher_data["user_rules"] + cipher_data["user_hints"])
    
    context = {
        'win': cipher_data["user_text"] == cipher_data["raw_text"],
        'cipher_text': cipher_data["cipher_text"],
        'user_text': cipher_data["user_text"],
        'hints': cipherWidget.format_hints(cipher_data["user_hints"]), 
        'rules': cipherWidget.format_rules(cipher_data["user_rules"]),
        'old_letter': cipher_data["old_letter"],
        'new_letter': cipher_data["new_letter"],
        'letters': [str(chr(i)) for i in range(65, 91)]
    }
    return render_template("cipher.html", **context)


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
    coursework_stream = open(appUtilities.get_file_path("coursework.yaml"), 'r')
    context = yaml.safe_load(coursework_stream)
    return render_template("coursework.html", **context)

# Projects page route
@app.route("/projects")
def projects():
    projects_stream = open(appUtilities.get_file_path("projects.yaml"), 'r')
    context = yaml.safe_load(projects_stream)
    return render_template("projects.html", **context)

if __name__ == "__main__":
    app.run()