# creates db
import sqlite3

# connect to a database (or create one if it doesn't exist)
conn = sqlite3.connect("./db/site.db")

# create a cursor object to interact with the database
cursor = conn.cursor()

# remove location with id

id = 26

cursor.execute("DELETE FROM locations WHERE id = ?", (id,))


conn.commit()
conn.close()
