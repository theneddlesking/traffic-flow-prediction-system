import sqlite3

import pandas as pd


class SQLiteDB:
    """A class to interact with an sqlite3 database."""

    def __init__(self, db_path: str):
        self.db_path = db_path
        self.models: set[DBModel] = set()

    def _connect(self):
        """Create a new database connection."""
        return sqlite3.connect(self.db_path)

    def execute_query(self, query: str, params=(), commit=False):
        """Execute a custom query on the database with parameterised inputs."""
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            if commit:
                conn.commit()
            return cursor.fetchall()

    def get_flow(self, location_id: int, time: str):
        """Get the flow at a location and time."""
        query = "SELECT flow FROM predictions WHERE location_id = ? AND time = ?"
        flow_as_all = self.execute_query(query, (location_id, time))
        return flow_as_all[0][0] if flow_as_all else None

    def rebuild_db(self):
        """Rebuild the database by dropping all tables and recreating them."""
        for model in self.models:
            model.rebuild_model()

    def add_model(self, model: "DBModel"):
        """Add a model to the database."""
        self.models.add(model)

    def init_db(self):
        """Initialise the database by rebuilding and then reinitialising all models with their default data."""
        # rebuild database
        self.rebuild_db()

        # initialise models
        for model in self.models:
            model.init_model()

    def init_if_not_exist(self):
        """Initialise the tables if they don't already exist."""
        # initialise models
        for model in self.models:
            model.init_if_not_exist()

    def copy_table(self, table_name: str, new_table_name: str):
        """Copy a table to a new table."""
        query = f"CREATE TABLE {new_table_name} AS SELECT * FROM {table_name}"
        self.execute_query(query, commit=True)

    def drop_table(self, table_name: str):
        """Drop a table."""
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.execute_query(query, commit=True)

    # NOTE: Proabbly should be in a separate class, but its kinda nice to have it here
    def create_table_from_df(
        self, df: pd.DataFrame, table_name: str, auto_increment=True
    ):
        """Add a dataframe to the database."""

        if auto_increment:
            df["id"] = range(1, len(df) + 1)

        with self._connect() as conn:
            df.to_sql(table_name, conn, if_exists="replace", index=False)


class DBModel:
    """A model for the database to interact with a specific table or set of tables."""

    def __init__(self, db: "SQLiteDB", table_name: str):
        self.db = db
        self.db.add_model(self)
        self.table_name = table_name

    def rebuild_model(self):
        """Rebuild the model by dropping all tables and recreating them."""
        raise NotImplementedError("This method should be implemented in a subclass.")

    def init_model(self):
        """Initialise the model with some default data."""
        raise NotImplementedError("This method should be implemented in a subclass.")

    def check_table_exists(self):
        """Check if a table exists."""
        table_exists_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{self.table_name}'"

        at_least_one_entry_query = f"SELECT COUNT(*) FROM {self.table_name}"

        exists = bool(self.db.execute_query(table_exists_query))

        if not exists:
            return False

        count = int(self.db.execute_query(at_least_one_entry_query)[0][0])

        at_least_one = count > 0

        return at_least_one

    def init_if_not_exist(self):
        """Initialise the model if it doesn't already exist."""
        if not self.check_table_exists():
            self.init_model()
