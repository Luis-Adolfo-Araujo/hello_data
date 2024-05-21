import psycopg2
from config import *

conn_str = f"host={DB_HOST} port={DB_PORT} dbname={DB_NAME} user={DB_USER} password={DB_PASS}"

def get_db_connection():
    try:
        conn = psycopg2.connect(conn_str)
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        return conn, cursor
    except psycopg2.Error as e:
        print("Error connecting to the database:", e)
        return None, None
