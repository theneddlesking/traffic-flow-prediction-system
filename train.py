import argparse
from data_loader import DataLoader
from data_visualiser import DataVisualiser
from model.model_result import ModelResult
from processing_step import ProcessingSteps

from model.model_trainer import ModelTrainer
from model.nn_model import Model
from model.model_builder import ModelBuilder
from model.training_config import TrainingConfig
from test import day_before, most_common_date


def get_model(model_name, units):
    if model_name == "gru":
        return Model(ModelBuilder.get_gru_with_heuristics(units), "basic_gru_model_with_heuristics")
    elif model_name == "lstm":
        return Model(ModelBuilder.get_lstm(units), "basic_lstm_model")
    elif model_name == "saes":
        return Model(ModelBuilder.get_saes(units), "basic_saes_model")
    else:
        raise ValueError(f"Unknown model name: {model_name}")

def main(model_name):
    lstm_units = [12, 64, 64, 1]
    gru_units = [12, 64, 64, 1]
    saes_units = [12, 400, 400, 400, 1]

    units = None
    if model_name == "gru":
        units = gru_units
    elif model_name == "lstm":
        units = lstm_units
    elif model_name == "saes":
        units = saes_units

    CSV = "./data/vic/ScatsOctober2006.csv"

    data_loader = DataLoader(
        CSV,
        "flow",
        [
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
                    "SITE_NUMBER": "site_number",
                }
            ),
            # remove bad location
            ProcessingSteps.filter_rows(
                lambda df: df["location"] != "AUBURN_RD N of BURWOOD_RD"
            ),
            ProcessingSteps.filter_rows(
                lambda df: df["location"] != "HIGH_ST NE of CHARLES_ST"
            ),
            # drop duplicates
            ProcessingSteps.drop_duplicates(),
            # get flow per period
            ProcessingSteps.get_flow_per_period(),
            # drop columns
            ProcessingSteps.filter_columns(["time", "flow", "location", "site_number"]),
        ],
    )

    print(data_loader.peek(data_loader.pre_processed_df))

    training_config = TrainingConfig(
        epochs=50,
        batch_size=256,
        lags=12,
        train_test_proportion=0.7,
        validation_split=0.05,
    )

    # define train data
    main_input_data = data_loader.create_train_test_split_from_df(
        training_config.train_test_proportion,
        training_config.lags,
        ["site_number"]
    )

    print(main_input_data.x_test[0].shape)

    model = get_model(model_name, units)

    # train model
    model, hist_df, main_input_data = ModelTrainer.train(
        main_input_data, training_config, model
    )

    y_true = main_input_data.y_test_original

    # predict
    y_preds = model.predict(main_input_data.x_test[0], main_input_data.scaler)

    # limit to one day
    y_true, y_preds = DataLoader.get_example_day(y_true, y_preds, training_config.lags)

    # create flow time df
    preds_df = DataLoader.create_flow_time_df(y_preds)

    # result
    results = [
        ModelResult(model, y_preds),
    ]

    # plot
    DataVisualiser.plot_results(results, y_true)

    # save plot
    DataVisualiser.save_plot(f'./results/visualisations/basic_{model_name}_model.png')

    # save model
    model.save("./saved_models")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train traffic prediction model")
    parser.add_argument(
        "--model", choices=["gru", "lstm", "saes"], required=True, help="Select which model to run"
    )
    args = parser.parse_args()

    main(args.model)