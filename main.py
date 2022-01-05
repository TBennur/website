from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

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
    print(request.args.get("selectionIndex"))
    return ("nothing")


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)