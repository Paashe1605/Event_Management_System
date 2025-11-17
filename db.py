import sqlite3

DB_PATH = "data/app.db"

def get_connection():
    return sqlite3.connect(DB_PATH)

def get_cursor(conn):
    return conn.cursor()

def close_connection(conn):
    conn.close()