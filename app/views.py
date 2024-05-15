from app import app
from flask import render_template

@app.route("/login")
def index():
    return render_template("public/login.html")