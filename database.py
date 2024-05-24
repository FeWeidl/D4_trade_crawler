import sqlite3
import json
import logging

def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    logging.info("Database connection established.")
    return conn, cursor

def create_table(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            user TEXT,
            attributes TEXT,
            price TEXT,
            UNIQUE(title, user, attributes, price)
        )
    ''')
    logging.info("Table created if not exists.")

def insert_item(cursor, item):
    try:
        cursor.execute('''
            INSERT INTO items (title, user, attributes, price) VALUES (?, ?, ?, ?)
        ''', (item['title'], item['user'], json.dumps(item['attributes']), item['price']))
        logging.info("Item inserted into database: %s", item['title'])
    except sqlite3.IntegrityError:
        logging.info("Item '%s' by '%s' already exists in the database.", item['title'], item['user'])
