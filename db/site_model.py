import pandas as pd
from data_loader import DataLoader
from db.sqlite_db import DBModel
from processing_step import ProcessingSteps


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

        csv = "./data/vic/ScatsOctober2006.csv"

        data_loader = DataLoader(
            csv,
            # arbitrary target
            "site_number",
            [
                # keep only necessary columns
                ProcessingSteps.filter_columns(
                    [
                        "SITE_NUMBER",
                        "LOCATION",
                        "NB_LATITUDE",
                        "NB_LONGITUDE",
                    ]
                ),
                # rename
                ProcessingSteps.rename_columns(
                    {
                        "SITE_NUMBER": "site_number",
                        "LOCATION": "name",
                        "NB_LATITUDE": "lat",
                        "NB_LONGITUDE": "long",
                    }
                ),
                # filter out bad location
                ProcessingSteps.filter_rows(
                    lambda df: df["name"] != "AUBURN_RD N of BURWOOD_RD"
                ),
                ProcessingSteps.filter_rows(
                    lambda df: df["name"] != "HIGH_ST NE of CHARLES_ST"
                ),
                # sort by location name
                ProcessingSteps.sort_by_column("name"),
                # drop duplicates
                ProcessingSteps.drop_duplicates(),
            ],
        )

        df = data_loader.pre_processed_df

        # add to db
        self.db.create_table_from_df(df, "locations")
