from data_loader import DataLoader
from data_visualiser import DataVisualiser
from model.model_result import ModelResult
from processing_step import ProcessingSteps

from model.model_trainer import ModelTrainer
from model.nn_model import Model
from model.model_builder import ModelBuilder
from model.training_config import TrainingConfig
from test import day_before, most_common_date


lstm_units = [12, 64, 64, 1]
gru_units = [12, 64, 64, 1]
saes_units = [12, 400, 400, 400, 1]

basic_model = Model(ModelBuilder.get_gru(gru_units), "basic_model")

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
        # TODO filter out dates before test date
        # filter out most common date and day before
        # filter to most common date or the day before
        ProcessingSteps.filter_rows(
            lambda df: df["DATE"].isin(
                [most_common_date(df), day_before(most_common_date(df))]
            ),
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
    ],
)

training_config = TrainingConfig(
    epochs=200,
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

# x shape

print(main_input_data.x_test.shape)

# train
basic_model, hist_df, main_input_data = ModelTrainer.train(
    main_input_data, training_config, basic_model
)

y_true = main_input_data.y_test_original

print(main_input_data.x_test.shape)

# predict
y_preds = basic_model.predict(main_input_data.x_test, main_input_data.scaler)

# limit to one day
y_true, y_preds = DataLoader.get_example_day(y_true, y_preds, training_config.lags)

# create flow time df
preds_df = DataLoader.create_flow_time_df(y_preds)

# result
results = [
    ModelResult(basic_model, y_preds),
]

# plot
DataVisualiser.plot_results(results, y_true)

# save plot
DataVisualiser.save_plot("./results/visualisations/basic_model.png")

# save model
basic_model.save("./saved_models")
