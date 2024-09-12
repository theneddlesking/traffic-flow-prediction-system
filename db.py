# creates db

import sqlite3

# connect to a database (or create one if it doesn't exist)
conn = sqlite3.connect("./db/site.db")

# create a cursor object to interact with the database
cursor = conn.cursor()

cursor.execute(
    """CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    site_number INTEGER,
                    time TEXT
                )"""
)

conn.commit()
conn.close()
