import pandas as pd
import sqlite3


def load_locations():
    CSV = "./data/vic/ScatsOctober2006.csv"

    df = pd.read_csv(CSV, encoding="utf-8")

    COLS_STR = "SITE_NUMBER,LOCATION,NB_LATITUDE,NB_LONGITUDE"

    cols = COLS_STR.split(",")

    cols_mapping = {
        "SITE_NUMBER": "site_number",
        "LOCATION": "name",
        "NB_LATITUDE": "lat",
        "NB_LONGITUDE": "long",
    }

    df = df[cols]

    df = df.rename(columns=cols_mapping)

    # connect to a database (or create one if it doesn't exist)
    conn = sqlite3.connect("./db/site.db")

    # remove duplicates
    df = df.drop_duplicates()

    # add index to df

    df["id"] = range(1, len(df) + 1)

    # add locations to db
    df.to_sql("locations", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    load_locations()
