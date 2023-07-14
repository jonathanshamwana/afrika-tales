from flask import Flask, render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)
Bootstrap(app)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/story", methods=["POST", "GET"])
def create_story():
    return render_template("create-story.html")

@app.route("/samples", methods=["POST", "GET"])
def get_samples():
    return render_template("samples.html")

if __name__ == "__main__":
    app.run(debug=True,port=9000)
