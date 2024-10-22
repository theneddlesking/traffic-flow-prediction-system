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
            lambda df: df["LOCATION"].isin(
                ["WARRIGAL_RD N of HIGH STREET_RD", "HIGH STREET_RD E of WARRIGAL_RD"]
            )
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

x_test = main_input_data.x_test

example_test = x_test[0]

print(f"example_test: {example_test}")

# scale

# scaled = main_input_data.scaler.inverse_transform(example_test)


prediction = model.predict(example_test, main_input_data.scaler)

print(f"prediction: {prediction}")
