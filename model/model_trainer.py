import pandas as pd

from tensorflow.python.keras.callbacks import History

from model.model_input_data import ModelInputData
from model.nn_model import Model
from model.training_config import TrainingConfig
import tensorflow as tf


class ModelTrainer:
    """Class to train models."""

    @staticmethod
    def train(
        model_input_data: ModelInputData, training_config: TrainingConfig, model: Model
    ):
        """Trains a model."""
        # NOTE: Not sure if the model passed in will be the Keras model itself or like a wrapper around it

        # but overall it will do something like

        # configure the model
        model.keras.compile(loss="mse", optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001), metrics=["mape"])

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
