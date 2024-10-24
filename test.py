import argparse
import asyncio
import math
import pandas as pd
from coordinate_offset import LAT_OFFSET, LONG_OFFSET
from data_loader import DataLoader
from processing_step import ProcessingSteps
from testing.solution import TravelTimeTestCaseSolution
from testing.test_case import TravelTimeTestCase
from testing.test_case_input import TravelTimeTestCaseInput
from testing.test_result import TravelTimeTestEvaluation
from testing.test_runner import TestRunner

from cache import default_cache

test_runner = TestRunner()

TRUE_DATA_CSV = "./true_data/cleanTrueData.csv"


def pad_time_strings(df: pd.DataFrame) -> pd.DataFrame:
    """Pad time strings with leading zeros."""
    # eg. 7:0 -> 07:00, 12:0 -> 12:00, 18:0 -> 18:00

    def replace_time(time: str) -> str:
        hour, minute = time.split(":")
        return f"{hour.zfill(2)}:{minute.zfill(2)}"

    df["time"] = df["time"].apply(replace_time)

    return df


def convert_time_taken_str_to_hours(df: pd.DataFrame) -> pd.DataFrame:
    """Convert time taken strings to hours."""
    # eg. 4 mins -> 0.0666667 hours, 1 hour 30 mins -> 1.5 hours

    def convert_time_taken(time_taken: str) -> float:
        time_taken = time_taken.split(" ")

        if len(time_taken) == 2:
            return float(time_taken[0]) / 60

        return float(time_taken[0]) + float(time_taken[3]) / 60

    df["time_taken"] = df["time_taken"].apply(convert_time_taken)

    return df


# Route_ID,START_LAT,START_LONG,END_LAT,END_LONG,Day,Time,Time_Taken
data_loader = DataLoader(
    TRUE_DATA_CSV,
    # arbitrary target
    "time",
    [
        # rename columns
        ProcessingSteps.rename_columns(
            {
                "Route_ID": "route_id",
                "START_LAT": "start_lat",
                "START_LONG": "start_long",
                "END_LAT": "end_lat",
                "END_LONG": "end_long",
                "Day": "day",
                "Time": "time",
                "Time_Taken": "time_taken",
            }
        ),
        # pad time strings
        pad_time_strings,
        # convert time taken strings to hours
        convert_time_taken_str_to_hours,
    ],
)

df = data_loader.pre_processed_df

# get all locations
locations = default_cache.site_controller.get_locations()


def get_location_id_from_lat_long(lat: float, long: float) -> int:
    """Get the location id from a latitude and longitude."""

    # apply offset
    lat += LAT_OFFSET
    long += LONG_OFFSET

    epsilon = 1e-9
    for location in locations:
        if math.isclose(location.lat, lat, abs_tol=epsilon) and math.isclose(
            location.long, long, abs_tol=epsilon
        ):
            return location.location_id

    return None


def test_model(model_name: str, limit: int = None) -> None:
    """Test the model."""

    # iter rows

    if limit is None:
        limit = len(df)

    for index, row in df.iterrows():
        if index == limit:
            break

        expected_output = TravelTimeTestCaseSolution(row["time_taken"])

        start_location_id = get_location_id_from_lat_long(
            float(row["start_lat"]), float(row["start_long"])
        )
        end_location_id = get_location_id_from_lat_long(
            float(row["end_lat"]), float(row["end_long"])
        )

        # could be from one of the bad locations
        if start_location_id is None or end_location_id is None:
            continue

        time_of_day = row["time"]

        input_data = TravelTimeTestCaseInput(
            start_location_id, end_location_id, time_of_day, model_name
        )

        # travel time test case
        travel_time_test_case = TravelTimeTestCase(
            f"Test case {index}", expected_output, input_data
        )

        test_runner.add_test_case(travel_time_test_case)

    results: list[TravelTimeTestEvaluation] = asyncio.run(test_runner.run())
    # results df

    result_dicts = [result.convert_to_dict() for result in results]

    results_df = pd.DataFrame(result_dicts)

    results_df.to_csv(f"./results/evaluations/{model_name}_results.csv", index=False)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Test the model.")

    parser.add_argument(
        "model_name",
        type=str,
        help="The name of the model to test.",
    )

    parser.add_argument(
        "--limit",
        type=int,
        help="The number of rows to test.",
        default=None,
    )

    args = parser.parse_args()

    model_name = args.model_name

    limit = args.limit

    test_model(model_name, limit)
