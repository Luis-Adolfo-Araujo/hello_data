from app import app
from flask import render_template

@app.route("/")
def index():
    return render_template("templates/public/index.html")