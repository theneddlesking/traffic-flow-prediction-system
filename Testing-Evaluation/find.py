import sqlite3

db_path = 'site.db'

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(locations)")
columns = cursor.fetchall()

for column in columns:
    print(column)
    
conn.close()
