import sqlite3
import logging
import json

def connect_db(db_file):
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        logging.info("Database connection established.")
        return conn, cursor
    except sqlite3.Error as e:
        logging.error(f"Error connecting to database: {e}")
        return None, None

def create_table(cursor):
    try:
        cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                            id TEXT PRIMARY KEY,
                            name TEXT,
                            attributes TEXT,
                            link TEXT
                          )''')
        logging.info("Table created if not exists.")
    except sqlite3.Error as e:
        logging.error(f"Error creating table: {e}")

def insert_item(cursor, item):
    try:
        cursor.execute('''INSERT INTO items (id, name, attributes, link) 
                          VALUES (?, ?, ?, ?)''', 
                          (item.get('id'), item.get('name'), json.dumps(item.get('attributes')), item.get('link')))
        logging.info(f"Item inserted into database: {item.get('name')}")
    except sqlite3.IntegrityError:
        logging.warning(f"Item already exists in database: {item.get('name')}")
    except sqlite3.Error as e:
        logging.error(f"Error inserting item: {e}")

def item_exists(cursor, item):
    try:
        cursor.execute("SELECT * FROM items WHERE id=?", (item.get('id'),))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f"Error checking item existence: {e}")
        return False
