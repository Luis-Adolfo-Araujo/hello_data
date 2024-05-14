from app import app

import psycopg2
from utils import *
from flask_cors import CORS 
from flask import Flask, Response, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity


CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route("/db", methods=["GET"])
def main():
    conn = get_db_connection()
    print(conn)
    return ''

def get_db_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except psycopg2.Error as e:
        print("Erro ao conectar ao banco de dados:", e)
        return None
