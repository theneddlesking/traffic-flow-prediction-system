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

# check csv

data_loader.save_df(data_loader.preprocess_df(data_loader.get_df()), "./current.csv")

training_config = TrainingConfig(
    epochs=25,
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

# not sure how shape is 881, from 2677 rows and 0.7 train test split
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
