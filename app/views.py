from app import app
from flask import render_template
from flask_login import login_required, current_user

@app.route("/login")
def index():
    return render_template("public/login.html")

@app.route("/profile")
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)