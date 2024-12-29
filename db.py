# database/db.py

import sqlite3

def create_connection(db_file):
    conn = sqlite3.connect(db_file)
    return conn

def create_table(conn):
    sql_create_requests_table = """
    CREATE TABLE IF NOT EXISTS requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        department TEXT,
        status TEXT
    );
    """
    cursor = conn.cursor()
    cursor.execute(sql_create_requests_table)
    conn.commit()

def insert_request(conn, user_id, message, department):
    sql = ''' INSERT INTO requests(user_id, message, department, status)
              VALUES(?,?,?,?) '''
    cursor = conn.cursor()
    cursor.execute(sql, (user_id, message, department, 'pending'))
    conn.commit()
    return cursor.lastrowid

def get_all_requests(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM requests")
    return cursor.fetchall()
