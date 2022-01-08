from flask import Flask, render_template, request, send_file, jsonify
from io import BytesIO
import base64
import imageFilter
from PIL import Image

images = {  "Beach": "beach.jpg",
            "Cave": "cave.png",
            "Foggy": "foggy.jpg",
            "Lake": "lake.jpg",
            "Microscope": "microscope.jpg",
            "Mountain": "mountain.png",
            "Pittsburgh": "pittsburgh.jpg",
            "Sunset": "sunset.jpg",
            "Train": "train.jpg",
            "Wasteland": "wasteland.jpg"
        }

pallets = { "Carpet Rose": ("carpet-rose-6.hex", 6),
            "Monometalic": ("monometalic-6.hex", 6),
            "Stormy": ("stormy-6.hex", 6),
            "Ammo": ("ammo-8.hex", 8), 
            "Dawnbringers": ("dawnbringers-8.hex", 8), 
            "Dreamscape": ("dreamscape-8.hex", 8), 
            "Just Parchment": ("just-parchment-8.hex", 8), 
            "Paper": ("paper-8.hex", 8), 
            "Rust Gold": ("rust-gold-8.hex", 8),
            "Dawnbringer": ("dawnbringer-16.hex", 16), 
            "Endesga": ("endesga-16.hex", 16), 
            "Feel The Sun": ("feel-the-sun-16.hex", 16), 
            "Galaxy Flame": ("galaxy-flame-16.hex", 16), 
            "Lost Century": ("lost-century-16.hex", 16), 
            "Ramp Rainbow": ("ramp-rainbow-16.hex", 16), 
            "Steam Lords": ("steam-lords-16.hex", 16),
            "AFR": ("afr-32.hex", 32), 
            "Endesga": ("endesga-32.hex", 32), 
            "Fantasy": ("fantasy-32.hex", 32), 
            "Hept": ("hept-32.hex", 32), 
            "Marshmellow": ("marshmellow-32.hex", 32), 
            "Nanner": ("nanner-32.hex", 32),
            "Comicscapes": ("comicscapes-50.hex", 50), 
            "Resurrect": ("resurrect-64.hex", 64),
            "Shido": ("shido-50.hex", 50)
        }

selections = {"image": None, "pallet": None}

def serve_pil_image(img):
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    encoded_img = base64.encodebytes(img_io.getvalue()).decode('ascii')
    response =  { 'Status' : 'Success', 'ImageBytes': encoded_img}
    print("Converted")
    return jsonify(response)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/stylizer")
def stylizer():
    return render_template("stylizer.html")

@app.route('/stylize-info', methods = ["GET"])
def stylize_info():
    print("Updated")
    selections["image"] = images[request.args.get("current_image")]
    selections["pallet_info"] = pallets[request.args.get("current_pallet")]
    return ("nothing")

@app.route('/stylize-button', methods = ["GET", "POST"])
def stylize_button():
    return serve_pil_image(imageFilter.convert_image(selections["image"], selections["pallet_info"][0], selections["pallet_info"][1]))

@app.route('/logger')
def logger():
    print("Log")
    return ("nothing")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)