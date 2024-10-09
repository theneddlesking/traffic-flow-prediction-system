import pandas as pd

from db.instance import site_controller
from routing.location import Location


class SpoofedModel:
    """Temporary spoof model for testing"""

    def __init__(self, name: str):
        self.name = name

    async def compute_flow(self, location_id: int, time: str) -> int:
        """Compute flow"""
        return 100

    def get_predictions_df(self) -> pd.DataFrame:
        """Get predictions of flow for all locations"""
        locations = site_controller.get_locations()

        # compute flow for each location
        flows = []

        for location in locations:
            flow = self.compute_flow(location.location_id, "12:00")
            flows.append((location.location_id, "12:00", flow))

        return pd.DataFrame(flows, columns=["location_id", "time", "flow"])
