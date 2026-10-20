import sqlite3
from contextlib import closing
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "main.db")

def get_connection():

    return sqlite3.connect(DB_PATH)

def execute(request, params = ()):

    with closing(get_connection()) as conn:
        with conn:
            cur = conn.execute(request, params)
            conn.commit()
            return cur.lastrowid

def fetch_all(request, params=()):

    with closing(get_connection()) as conn:
        cur = conn.execute(request, params)
        return cur.fetchall()

def fetch_one(request, params=()):

    with closing(get_connection()) as conn:
        cur = conn.execute(request, params)
        return cur.fetchone()