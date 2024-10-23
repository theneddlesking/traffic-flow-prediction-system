import pandas as pd
from data_loader import DataLoader
from db.sqlite_db import DBModel, SQLiteDB
from model.nn_model import Model
from model.real_time_source import RealTimeSource
from time_utils import TimeUtils


class FlowPredictorModel(DBModel):
    """A model for the database to interact with the traffic flow table."""

    def __init__(
        self, db: SQLiteDB, model: Model, real_time_sources: list[RealTimeSource]
    ):
        # ! Assumes that model_name is passed in safely, NOT USER FACING
        # TODO is there a better way to handle this?
        super().__init__(db, f"{model.name}_predictions")

        self.real_time_sources = real_time_sources

        self.model = model

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

    def get_predictions_for_source(self, real_time_data: RealTimeSource):
        """Get predictions for a real time source."""

        preds = []

        # TODO utilise batching to speed up predictions

        for i in range(0, len(real_time_data.day_of_flow_data)):

            x_test, scaler = DataLoader.load_from_real_time_source(real_time_data, i)

            # get predictions
            prediction = self.model.predict_from_last_n_batch([x_test], scaler)

            # add to preds
            preds.append(prediction[0])

        return preds

    def init_model(self):
        """Initialise the model with default predictions."""

        locations_preds = {}

        for real_time_source in self.real_time_sources:
            preds = self.get_predictions_for_source(real_time_source)

            location = real_time_source.location_id

            locations_preds[location] = preds

        # create df
        df_rows = []

        for location, preds in locations_preds.items():
            for i, pred in enumerate(preds):
                df_rows.append(
                    {
                        "location_id": location,
                        "time": TimeUtils.convert_minute_index_to_str(i),
                        "flow": pred,
                    }
                )

        df = pd.DataFrame(df_rows)

        # add to db
        self.db.create_table_from_df(df, self.table_name)
