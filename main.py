import pandas as pd
from data_loader import DataLoader
from data_visualiser import DataVisualiser
from processing_step import ProcessingSteps
from time_utils import TimeUtils

from model.model_trainer import ModelTrainer
from model.nn_model import Model
from model.model_builder import ModelBuilder
from model.training_config import TrainingConfig


lstm_units = [12, 64, 64, 1]
gru_units = [12, 64, 64, 1]
saes_units = [12, 400, 400, 400, 1]

basic_model = Model(ModelBuilder.get_gru(lstm_units), "basic_model")

CSV = "./data/vic/ScatsOctober2006.csv"


def get_flow_per_period(df: pd.DataFrame, period_in_minutes=15) -> pd.DataFrame:
    """Get flow per period"""
    ouput_df_rows = []

    # iter each row
    for _, row in df.iterrows():

        # get flow
        flow = row["V00":"V95"]

        # get 15 minutes
        for i in range(0, 96, 1):

            ouput_df_rows.append(
                {
                    "time": TimeUtils.convert_minute_index_to_str(i, period_in_minutes),
                    "flow": flow[i],
                },
            )

    return pd.DataFrame(ouput_df_rows)


data_loader = DataLoader(
    CSV,
    "flow",
    [
        # filter only LOCATION = "WARRIGAL_RD N of HIGH STREET_RD" for now
        ProcessingSteps.filter_rows(
            lambda df: df["LOCATION"] == "WARRIGAL_RD N of HIGH STREET_RD"
        ),
        # drop duplicates
        ProcessingSteps.drop_duplicates(),
        # get flow per period
        get_flow_per_period,
    ],
)

training_config = TrainingConfig(
    epochs=10,
    batch_size=256,
    lags=12,
    train_test_proportion=0.7,
    validation_split=0.05,
)

basic_model, hist_df, main_input_data = ModelTrainer.train(
    data_loader, training_config, basic_model
)

# save image

names = ["GRU"]

y_true = main_input_data.y_test_original

# shape

y_preds = basic_model.keras.predict(main_input_data.x_test)

# reshape

y_preds = main_input_data.scaler.inverse_transform(y_preds)

# limit to 96 (number of 15 minute periods in a day)

lags = training_config.lags

y_true = y_true[96 - lags : 96 * 2 - lags]
y_preds = y_preds[96 - lags : 96 * 2 - lags]

# inverse transform

# plot
DataVisualiser.plot_results(
    y_true,
    [y_preds],
    names,
    "./results/visualisations/plot.png",
)

# imagine that these are the last 12 recorded flows for the day at a given location
# we want to know what the flow will be in the next period
# so we use the model to predict the flow for the next period

# imagine in the real world
# this data would be coming from a live feed!

# for our project, we can simply use the last 24 hour period in the test data

dummy_last_12 = [
    10,
    12,
    15,
    20,
    25,
    30,
    35,
    40,
    45,
    50,
    55,
    60,
]

# normalise

normalised = []

for i in range(lags):
    normalised.append(
        main_input_data.scaler.transform(
            [[dummy_last_12[i]]],
        )[
            0
        ][0],
    )

dummy_last_12 = [normalised]

# reshape

dummy_last_12 = pd.DataFrame(dummy_last_12)

dummy_last_12 = dummy_last_12.values.reshape(1, lags, 1)

# predict

next_res = basic_model.keras.predict(dummy_last_12)

# inverse transform

next_res = main_input_data.scaler.inverse_transform(next_res)

# reshape to just int

next_res = int(next_res[0][0])

print(next_res)
