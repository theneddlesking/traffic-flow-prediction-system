import pandas as pd
from data_loader import DataLoader
from data_visualiser import DataVisualiser
from model.model_result import ModelResult
from processing_step import ProcessingSteps
from time_utils import TimeUtils

from model.model_trainer import ModelTrainer
from model.nn_model import Model
from model.model_builder import ModelBuilder
from model.training_config import TrainingConfig


lstm_units = [12, 64, 64, 1]
gru_units = [12, 64, 64, 1]
saes_units = [12, 400, 400, 400, 1]

basic_model = Model(ModelBuilder.get_gru(gru_units), "basic_model")

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

# train
basic_model, hist_df, main_input_data = ModelTrainer.train(
    data_loader, training_config, basic_model
)

y_true = main_input_data.y_test_original

# shape
y_preds = basic_model.predict(main_input_data.x_test)

# reshape
y_preds = main_input_data.scaler.inverse_transform(y_preds)

# limit to one day
y_true, y_preds = DataLoader.get_example_day(y_true, y_preds, 12)

# result
results = [
    ModelResult(basic_model, y_preds),
]

# plot
DataVisualiser.plot_results(results, y_true)

# save plot
DataVisualiser.save_plot("./results/visualisations/basic_model.png")

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

next_res = basic_model.predict_from_last_n(dummy_last_12, main_input_data.scaler)

print(next_res)

# save model
basic_model.save("./saved_models")
