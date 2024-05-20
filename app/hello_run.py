from config import *
import psycopg2
from flask import Response, request, jsonify, session, render_template, flash, Blueprint, redirect, url_for
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)
main = Blueprint('main', __name__)
conn_str = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

@auth.route("/", methods=["GET"])
def main_route():
    return render_template("public/login.html")

@auth.route("/login", methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    conn, cursor = get_db_connection()

    if conn is None or cursor is None:
        return jsonify({"error": "Failed to connect to the database"}), 500

    try:
        query = '''SELECT * FROM paciente WHERE email = %s;'''
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        print("user: ", user)
        if user is None or not check_password_hash(user['password'], password):
            flash("Please check your login details and try again")
            return redirect(url_for('auth.main_route'))
        login_user(user)
        return redirect(url_for('auth.home')), 200
    except psycopg2.Error as e:
        print("Error during query execution:", e)
        return jsonify({"error": "Error during query execution"}), 500
    finally:
        cursor.close()
        conn.close()

def get_db_connection():
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, cursor
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None, None
