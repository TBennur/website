from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    
@app.route("/stylizer")
def stylizer():
    return render_template("stylizer.html")

@app.route('/stylize-button', methods = ["GET"])
def stylize_button():
    print(request.args.get("pallet_selected"))
    print(request.args.get("current_image"))
    print(request.args.get("current_pallet_size"))
    print(request.args.get("current_pallet"))
    return ("nothing")

@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)