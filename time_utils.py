class TimeUtils:

    # TODO not sure where to put this
    # Utils in general are kinda of an anti-pattern

    @staticmethod
    def convert_minute_index_to_str(i, period_in_minutes=15):
        """Convert a minute index to a string representation of the time."""
        minutes_in_hour = 60

        period_per_hour = minutes_in_hour // period_in_minutes

        hours = i // period_per_hour
        minutes = (i % period_per_hour) * period_in_minutes

        # pad 0s to make it 2 digits
        hours_str = str(hours).zfill(2)
        minutes_str = str(minutes).zfill(2)

        return f"{hours_str}:{minutes_str}"

    @staticmethod
    def convert_str_to_minute_index(time_str: str, period_in_minutes=15):
        """Convert a string representation of the time to a minute index."""
        hours, minutes = map(int, time_str.split(":"))

        minutes_in_hour = 60

        period_per_hour = minutes_in_hour // period_in_minutes

        return hours * period_per_hour + minutes // period_in_minutes
