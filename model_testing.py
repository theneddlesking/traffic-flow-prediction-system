import numpy as np
from data_loader import DataLoader
from model.model_builder import ModelBuilder
from model.nn_model import Model
from model.training_config import TrainingConfig
from processing_step import ProcessingSteps


model = Model.load("./saved_models/basic_model.keras")


lstm_units = [12, 64, 64, 1]
gru_units = [12, 64, 64, 1]
saes_units = [12, 400, 400, 400, 1]


CSV = "./data/vic/ScatsOctober2006.csv"

data_loader = DataLoader(
    CSV,
    "flow",
    [
        # filter only some locations
        ProcessingSteps.filter_rows(
            lambda df: df["LOCATION"].isin(["WARRIGAL_RD N of HIGH STREET_RD"])
        ),
        # categorise location
        ProcessingSteps.categorise_column("LOCATION"),
        # rename columns
        ProcessingSteps.rename_columns(
            {
                "LOCATION": "location",
            }
        ),
        # remove bad location
        ProcessingSteps.filter_rows(
            lambda df: df["location"] != "AUBURN_RD N of BURWOOD_RD"
        ),
        # drop duplicates
        ProcessingSteps.drop_duplicates(),
        # get flow per period
        ProcessingSteps.get_flow_per_period(),
        # drop columns
        ProcessingSteps.filter_columns(["time", "flow", "location"]),
        # TODO filter out dates before test date
    ],
)

training_config = TrainingConfig(
    epochs=50,
    batch_size=256,
    lags=12,
    train_test_proportion=0.7,
    validation_split=0.05,
)

# train
main_input_data = data_loader.create_train_test_split_from_df(
    training_config.train_test_proportion,
    training_config.lags,
)

x_test = [
    [32, 30, 20, 19, 16, 25, 10, 9, 6, 6, 6, 12],
    [6, 12, 11, 7, 8, 4, 10, 7, 10, 12, 20, 43],
    # bigs one
    [46, 53, 53, 43, 59, 75, 100, 103, 125, 141, 148, 175],
]

prediction = model.predict_from_last_n_batch(x_test, main_input_data.scaler)

print(f"prediction: {prediction}")
