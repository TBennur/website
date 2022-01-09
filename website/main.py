from flask import Flask, render_template, request, jsonify
from io import BytesIO
import base64
import yaml
from stylizer import imageFilter


# Setup webpage and import constants
app = Flask(__name__)
conversion_stream = open("stylizer/stylizeNameConversion.yaml", 'r')
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
    
    current_request_info = request.get_data().decode('UTF-8').split("|")
    current_image = conversion_dictionary[current_request_info[0][1:]]
    current_pallet_info = conversion_dictionary[current_request_info[1][0:len(current_request_info[1]) - 1]]
    
    img = imageFilter.convert_image(current_image, current_pallet_info['filename'], current_pallet_info['size'])
    
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    encoded_img = base64.encodebytes(img_io.getvalue()).decode('ascii')
    
    response =  { 'Status' : 'Success', 'ImageBytes': encoded_img}
    
    return jsonify(response)

# About page route
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)