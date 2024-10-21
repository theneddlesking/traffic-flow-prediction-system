import pandas as pd
from model.nn_model import Model
from time_utils import TimeUtils


class RealTimeSource:
    """Spoofs the real-time source for traffic flow for testing purposes."""

    def __init__(
        self,
        day_of_flow_data: list[int],
        lag_flow_data_from_day_before: list[int],
        model: Model,
    ):
        self.lag_flow_data_from_day_before = lag_flow_data_from_day_before
        self.day_of_flow_data = day_of_flow_data

        self.model = model

        self.lags = len(lag_flow_data_from_day_before)

        self.minutes_per_period = 60 * 24 / len(day_of_flow_data)

    def get_lag_input_data_for_time(self, time_index: int) -> list[int]:
        """Get subset of data at the correct time index"""

        all_data = self.lag_flow_data_from_day_before + self.day_of_flow_data

        offset_index = time_index + self.lags

        return all_data[offset_index - self.lags : offset_index]

    async def compute_flow(self, location_id: int, time: str) -> int:
        """Compute flow"""

        # TODO also use location_id for general model

        # get subset of data

        time_index = TimeUtils.convert_str_to_minute_index(
            time, period_in_minutes=self.minutes_per_period
        )

        data = self.get_lag_input_data_for_time(time_index)

        # predict flow
        flow = self.model.predict(data)

        return flow

    def get_predictions_df(self) -> pd.DataFrame:
        """Get predictions of flow for all times"""

        # TODO

        return pd.DataFrame()
