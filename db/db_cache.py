from db.flow_model import FlowPredictorModel
from db.site_controller import SiteController
from db.site_model import SiteModel
from db.sqlite_db import SQLiteDB
from model.model_manager import ModelManager
from model.real_time_source import RealTimeSource
from db.flow_controller import FlowController


class DBCache:
    """Uses the DB as a cache for saving model predictions to save time and computation."""

    def __init__(
        self,
        db_path: str,
        real_time_source: RealTimeSource,
        model_manager: ModelManager,
    ):
        self.db = SQLiteDB(db_path)

        self.site_controller = SiteController(SiteModel(self.db))

        self.flow_controller = FlowController(
            [
                FlowPredictorModel(self.db, model, real_time_source)
                for model in model_manager.models
            ]
        )
