class RealTimeSource:
    """Spoofs the real-time source for traffic flow at a particular location for testing purposes.  \
        You can imagine it as a sensor that provides data for a location."""

    def __init__(
        self,
        day_of_flow_data: list[int],
        lag_flow_data_from_day_before: list[int],
        location_id: int,
        location_name: str,
    ):
        self.lag_flow_data_from_day_before = lag_flow_data_from_day_before
        self.day_of_flow_data = day_of_flow_data
        self.location_id = location_id
        self.location_name = location_name

        self.lags = len(lag_flow_data_from_day_before)

        self.minutes_per_period = 60 * 24 / len(day_of_flow_data)

    def get_lag_input_data_for_time(self, time_index: int) -> list[int]:
        """Get subset of data at the correct time index"""

        all_data = self.lag_flow_data_from_day_before + self.day_of_flow_data

        return all_data[time_index : time_index + self.lags]
