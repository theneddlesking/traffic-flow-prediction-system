# build data, train model and run model for specific location

import argparse

import pandas as pd

from vic_convert import (
    clean_test_train,
    create_test_train_from_location,
    convert_minute_index_to_str,
)
from train import train_model_for_location
from main import run_model


def build_train_run(location, model="gru"):

    # create test train data
    create_test_train_from_location(location)

    # train model
    train_model_for_location(location, ".", model, {"epochs": 10, "batch": 256})

    # run model
    predictions = run_model(location, [model], save_image=False)

    df = pd.DataFrame(predictions, columns=[model])

    # add time column

    df["time"] = [convert_minute_index_to_str(i, 5) for i in range(288)]

    # clean test train data
    clean_test_train()

    return df


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--location",
        type=str,
        help="Location to extract data from",
    )

    args = parser.parse_args()

    # check if location is provided
    if not args.location:
        raise ValueError("Location is required")

    build_train_run(args.location)
