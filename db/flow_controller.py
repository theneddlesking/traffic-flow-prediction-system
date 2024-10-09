from db.controller import Controller
from db.flow_model import FlowPredictorModel


class FlowController(Controller):
    """FlowController class"""

    def __init__(self, db_model: FlowPredictorModel):
        super().__init__(db_model)
        self.model: FlowPredictorModel

    def get_flow(self, location_id: int, time: str):
        """Get flow"""
        return self.model.get_flow(location_id, time)

    def get_max_flow(self, location_id: int):
        """Get max flow assuming that flows have been computed for the location."""

        # NOTE: This assumes that the flows have been computed for the location and are stored in the db

        all_flows = self.model.get_flows(location_id)

        flow_amounts = [flow[1] for flow in all_flows]

        if flow_amounts:
            return max(flow_amounts)

        return None

    def compute_flow(self, location_id: int, time: str):
        """Compute flow, caching all flows for the location."""
        return self.model.model.compute_flow(location_id, time)
