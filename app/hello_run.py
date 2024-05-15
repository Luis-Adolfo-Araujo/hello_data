from app import app

import psycopg2
from utils import *
from flask_cors import CORS 
from flask import Flask, Response, request, jsonify
from flask_jwt_extended import create_access_token, JWTManager, jwt_required, get_jwt_identity

CORS(app)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
conn_str = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

@app.route("/db", methods=["GET"])
def main():
    get_db_connection()
    return ''

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
