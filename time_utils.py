class TimeUtils:

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

    @staticmethod
    def round_time_to_nearest_quarter(time_str: str):
        """Round time to nearest quarter."""
        # eg. 12:07 -> 12:00
        hours = int(time_str.split(":")[0])
        minutes = int(time_str.split(":")[1])

        # 0-8 -> 0, 8-23 -> 15, 23-38 -> 30, 38-53 -> 45, 53-60 -> 0 (next hour)

        if minutes <= 8:
            minutes = 0
        elif minutes <= 23:
            minutes = 15
        elif minutes <= 38:
            minutes = 30
        elif minutes <= 53:
            minutes = 45
        else:
            minutes = 0
            # increment hour
            hours += 1

        # with padding 0s
        return f"{str(hours).zfill(2)}:{str(minutes).zfill(2)}"
