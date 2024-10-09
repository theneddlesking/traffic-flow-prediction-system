import pandas as pd


class SpoofedModel:
    """Temporary spoof model for testing"""

    def __init__(self, name: str):
        self.name = name

    async def compute_flow(self, location_id: int, time: str) -> int:
        """Compute flow"""
        return 100

    def get_predictions_df(self) -> pd.DataFrame:
        """Get predictions of flow for all locations"""
        # TODO
        return pd.DataFrame()
