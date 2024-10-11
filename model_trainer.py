import pandas as pd

from tensorflow.python.keras.callbacks import History

from data_loader import DataLoader
from nn_model import Model
from training_config import TrainingConfig


class ModelTrainer:
    """Class to train models."""

    @staticmethod
    def train(data_loader: DataLoader, training_config: TrainingConfig, model: Model):
        """Trains a model."""
        # NOTE: Not sure if the model passed in will be the Keras model itself or like a wrapper around it

        # but overall it will do something like

        df = data_loader.get_df()

        processed_df = data_loader.preprocess_df(df)

        if not data_loader.df_contains_target(processed_df):
            raise ValueError(
                "Target column not found in data frame. Make sure the target column is in the data frame after preprocessing."
            )

        model_input_data = data_loader.create_train_test_split_from_df(
            processed_df,
            training_config.train_test_proportion,
            data_loader.target,
            training_config.lags,
        )

        # configure the model
        model.keras.compile(loss="mse", optimizer="rmsprop", metrics=["mape"])

        hist: "History" = model.keras.fit(
            model_input_data.x_train,
            model_input_data.y_train,
            batch_size=training_config.batch_size,
            epochs=training_config.epochs,
            validation_split=training_config.validation_split,
        )

        # load into a df for evaluation
        hist_df = pd.DataFrame(hist.history)

        return model, hist_df, model_input_data
