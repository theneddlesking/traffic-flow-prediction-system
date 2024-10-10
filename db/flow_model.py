from db.sqlite_db import DBModel, SQLiteDB
from db.spoofed_model import SpoofedModel


class FlowPredictorModel(DBModel):
    """A model for the database to interact with the traffic flow table."""

    def __init__(self, db: SQLiteDB, model: SpoofedModel):
        super().__init__(db)

        self.model = model
        # ! Assumes that model_name is passed in safely, NOT USER FACING
        # TODO is there a better way to handle this?
        self.table_name = f"{model.name}_predictions"

    def get_flow(self, location_id: int, time: str) -> int | None:
        """Get the flow at a location and time."""
        query = f"SELECT flow FROM {self.table_name} WHERE location_id = ? AND time = ?"
        flow_as_all = self.db.execute_query(query, (location_id, time))
        return flow_as_all[0][0] if flow_as_all else None

    def get_flows(self, location_id: int) -> list[tuple[int]]:
        """Get all flows at a location for all times."""
        query = f"SELECT time, flow FROM {self.table_name} WHERE location_id = ?"
        return self.db.execute_query(query, (location_id,))

    def rebuild_model(self):
        """Rebuild the database by dropping all tables and recreating them."""

        # PREDICTIONS

        # drop table
        self.db.execute_query(
            f"DROP TABLE IF EXISTS {self.table_name}",
            commit=True,
        )

        # rebuild table
        self.db.execute_query(
            f"""CREATE TABLE IF NOT EXISTS {self.table_name} (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            location_id INTEGER,
                            time TEXT,
                            flow INTEGER,
                            FOREIGN KEY (location_id) REFERENCES locations (id)
                        )""",
            commit=True,
        )

    def init_model(self):
        """Initialise the model with default predictions."""
        df = self.model.get_predictions_df()

        self.db.create_table_from_df(df, self.table_name)
