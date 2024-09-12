# creates db
import sqlite3


def init_db():
    # connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect("./db/site.db")

    # create a cursor object to interact with the database
    cursor = conn.cursor()

    # drop tables
    cursor.execute("DROP TABLE IF EXISTS locations")

    # location table
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS locations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        site_number INTEGER,
                        name TEXT,
                        lat REAL,
                        long REAL
                    )"""
    )

    cursor.execute("DROP TABLE IF EXISTS predictions")

    # predictions table that uses locations id as a foreign key
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS predictions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location_id INTEGER,
                        time TEXT,
                        flow INTEGER,
                        FOREIGN KEY (location_id) REFERENCES locations (id)
                    )"""
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
