import sqlite3

DB_PATH = "main.db"

def get_connection():

    return sqlite3.connect(DB_PATH)

def set_group_by_chat_id(chat_id, group):

    with get_connection() as conn:

        conn.executescript(
            'INSERT INTO groups(chat_id, "group") VALUES(?, ?)',
            (chat_id, group)
        )


def get_all_groups(chat_id, group):

    with get_connection() as conn:

        conn.executescript(
            'SELECT * FROM groups'
        )