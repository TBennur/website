from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

stylizer_status = {"Pallet Selected": False, "Current Image": "Beach", "Current Pallet Size": None, "Current Pallet": None}

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/stylizer")
def stylizer():
    stylizer_status["Pallet Selected"] = False
    stylizer_status["Current Image"] = "Beach"
    stylizer_status["Current Pallet Size"] = None
    stylizer_status["Current Pallet"] = None
    return render_template("stylizer.html")

@app.route('/stylize-button')
def stylize_button():
    print(stylizer_status)
    return ("nothing")


@app.route('/update-stylize-information', methods=["GET"])
def update_stylize_information():
    selection_type = request.args.get("selection_type")
    if selection_type == "Image Selected":
        image_selection = request.args.get("image_selection")
        stylizer_status["Current Image"] = image_selection
    elif selection_type == "Deselect Pallet Size":
        stylizer_status["Pallet Selected"] = False
        stylizer_status["Current Pallet Size"] = None
        stylizer_status["Current Pallet"] = None
    elif selection_type == "Select Pallet Size":
        pallet_size = request.args.get("pallet_size")
        stylizer_status["Current Pallet Size"] = pallet_size
    elif selection_type == "Deselect Pallet":
        stylizer_status["Pallet Selected"] = False
        stylizer_status["Current Pallet"] = None
    elif selection_type == "Select Pallet":
        pallet_name = request.args.get("pallet_name")
        stylizer_status["Pallet Selected"] = True
        stylizer_status["Current Pallet"] = pallet_name
    else:
        print("Invalid Update Call")
    return ("nothing")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)