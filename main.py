import pandas as pd
from data_loader import DataLoader
from model_trainer import ModelTrainer
from nn_model import Model
from model_builder import ModelBuilder
from processing_step import ProcessingSteps
from time_utils import TimeUtils
from training_config import TrainingConfig


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

        date = row["DATE"]

        # get 15 minutes
        for i in range(0, 96, 1):

            ouput_df_rows.append(
                {
                    "time": date
                    + " "
                    + TimeUtils.convert_minute_index_to_str(i, period_in_minutes),
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

training_config = TrainingConfig(epochs=10, batch_size=256)

basic_model, hist_df, main_input_data = ModelTrainer.train(
    data_loader, training_config, basic_model
)

print(hist_df)
