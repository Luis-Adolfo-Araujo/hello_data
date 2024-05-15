from app import app
import psycopg2
from config import *
from flask_cors import CORS
import jwt
from flask import Response, request, jsonify, session, render_template
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from functools import wraps

CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
conn_str = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

app.config['SECRET_KEY'] = SECRET_KEY

@app.route("/", methods=["GET"])
def main():
    # if not session.get('logged_in'):
    return render_template("public/login.html")
    # else:
        # return 'user already logged'

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.args.get('token')
        print(token)
        if not token:
            return jsonify({'Alert!':'Token missing'})
        try:
            return jwt.decode(token, app.config['SECRET_KEY'])
        except jwt.exceptions.PyJWTError as e:
            print(f"JWT error: {e}")
            return None
    return decorated

@app.route("/home")
@token_required
def home():
    return 'HOME'

@app.route("/login", methods=["POST"])
def login():
    try:
        if request.form['email'] and request.form['password'] == '123':
            print(request.form['email'])
            session['logged_in'] = True
            token = jwt.encode({
                'email': request.form['email'],
                'expiration': str(datetime.utcnow() + timedelta(seconds=25))
            },
            app.config['SECRET_KEY'])
            return jsonify({'token': token})
    except jwt.exceptions.PyJWTError as e:
        print(f"JWT error: {e}")
        return None

def get_db_connection():
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()
        print(db_version)
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
