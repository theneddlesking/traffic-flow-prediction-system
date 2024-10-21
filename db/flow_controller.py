from db.controller import Controller
from db.flow_model import FlowPredictorModel
from model.nn_model import Model


class FlowController(Controller):
    """FlowController class"""

    def __init__(self, db_models: list[FlowPredictorModel]):
        super().__init__(None)
        self.model: None
        self.db_models = db_models

    def get_matching_db_model(self, model: Model) -> FlowPredictorModel:
        """Get matching db model"""
        for db_model in self.db_models:
            if db_model.model.name == model.name:
                return db_model

        return None

    def get_flow(self, location_id: int, time: str, model: Model):
        """Get flow"""
        db_model = self.get_matching_db_model(model)
        return db_model.get_flow(location_id, time)

    def get_max_flow(self, location_id: int, model: Model):
        """Get max flow assuming that flows have been computed for the location."""

        db_model = self.get_matching_db_model(model)

        # NOTE: This assumes that the flows have been computed for the location and are stored in the db

        all_flows = db_model.get_flows(location_id)

        flow_amounts = [flow[1] for flow in all_flows]

        if flow_amounts:
            return max(flow_amounts)

        return None

    def compute_flow(self, location_id: int, time: str, model: Model):
        """Compute flow, caching all flows for the location."""
        db_model = self.get_matching_db_model(model)
        return db_model.real_time_data.compute_flow(location_id, time)
