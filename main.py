from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

current_selections = {"current_image": 1}

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/stylizer")
def stylizer():
    return render_template("stylizer.html")

@app.route('/stylize-button')
def stylize_button():
    print ("Hi")
    return ("nothing")

@app.route('/selection-test', methods=["GET"])
def selection_test():
    selection = request.args.get("selectionIndex")
    if selection != "Please Select an Image":
        current_selections["current_image"] = int(selection)
    print(current_selections["current_image"])
    return ("nothing")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)