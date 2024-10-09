import pandas as pd
from db.sqlite_db import DBModel


class SiteModel(DBModel):
    """SiteModel class"""

    def get_locations(self):
        """Get all locations."""
        query = "SELECT id, site_number, name, lat, long FROM locations"
        return self.db.execute_query(query)

    def get_location(self, location_id: int) -> tuple:
        """Get a location."""
        query = "SELECT id, site_number, name, lat, long FROM locations WHERE id = ?"
        location_as_all = self.db.execute_query(query, (location_id,))
        return location_as_all[0] if location_as_all else None

    def rebuild_model(self):
        """Rebuild the database by dropping all tables and recreating them."""
        # LOCATIONS

        # drop table
        self.db.execute_query("DROP TABLE IF EXISTS locations", commit=True)

        # rebuild table
        self.db.execute_query(
            """CREATE TABLE IF NOT EXISTS locations (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            site_number INTEGER,
                            name TEXT,
                            lat REAL,
                            long REAL
                        )""",
            commit=True,
        )

    def init_model(self):
        """Initialise the model with default locations."""

        # TODO refactor this out to some kind of data loader

        csv = "./data/vic/ScatsOctober2006.csv"

        df = pd.read_csv(csv, encoding="utf-8")

        cols_str = "SITE_NUMBER,LOCATION,NB_LATITUDE,NB_LONGITUDE"

        cols = cols_str.split(",")

        cols_mapping = {
            "SITE_NUMBER": "site_number",
            "LOCATION": "name",
            "NB_LATITUDE": "lat",
            "NB_LONGITUDE": "long",
        }

        df = df[cols]

        df = df.rename(columns=cols_mapping)

        # remove duplicates
        df = df.drop_duplicates()

        # add to db
        self.db.create_table_from_df(df, "locations")
