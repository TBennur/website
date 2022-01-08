from flask import Flask, render_template, request, send_file, jsonify
from io import BytesIO
import base64
import yaml
from stylizer import imageFilter


selections = {"image": None, "pallet": None}

app = Flask(__name__)

conversion_stream = open("stylizer/stylizeNameConversion.yaml", 'r')
conversion_dictionary = yaml.safe_load(conversion_stream)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/stylizer")
def stylizer():
    return render_template("stylizer.html")

@app.route('/stylize-info', methods = ["GET"])
def stylize_info():
    selections["image"] = conversion_dictionary[request.args.get("current_image")]
    selections["pallet_info"] = conversion_dictionary[request.args.get("current_pallet")]
    return ("nothing")

@app.route('/stylize-button')
def stylize_button():
    img = imageFilter.convert_image(selections["image"], selections["pallet_info"]['filename'], selections["pallet_info"]['size'])
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    encoded_img = base64.encodebytes(img_io.getvalue()).decode('ascii')
    response =  { 'Status' : 'Success', 'ImageBytes': encoded_img}
    return jsonify(response)

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)