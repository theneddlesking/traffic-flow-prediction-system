import os
import keras
from numpy import ndarray
import pandas as pd
from sklearn.discriminant_analysis import StandardScaler


class Model:
    """Neural Network Model"""

    def __init__(self, keras_model: keras.models.Model, name: str):
        self.keras = keras_model
        self.name = name

    def save(self, directory: str):
        """Save the model to disk."""
        path = f"{directory}/{self.name}.keras"
        self.keras.save(path)

    @staticmethod
    def load(path: str):
        """Load the model from disk."""

        # without extension
        name = os.path.basename(path).split(".")[0]

        return Model(keras.models.load_model(path), name)

    def predict(self, data: list, scaler: StandardScaler) -> ndarray:
        """Predict the output from the input data and automatically inverse transform it."""
        res: ndarray = self.keras.predict(data)

        # inverse transform
        inverse = scaler.inverse_transform(res)

        return inverse.reshape(1, -1)[0]

    def predict_from_last_n_batch(
        self, data_batch: list[list[int]], scaler: StandardScaler
    ) -> list[int]:
        """Predict the output for a batch of lists, where each list is a 1D array of flow values.
        The output is a list of predicted actual (unnormalized) values.
        """

        # ensure all lists in the batch have the same length as the required lags
        lags = self.keras.input_shape[1]

        for data in data_batch:
            if len(data) != lags:
                raise ValueError(
                    f"Each data input must have {lags} lags, but got {len(data)}"
                )

        # normalise the entire batch
        normalised_batch = []
        for data in data_batch:
            normalised_batch.append([scaler.transform([[val]])[0][0] for val in data])

        # convert to df
        x = pd.DataFrame(normalised_batch)

        # reshape to the input shape for the model: (batch_size, lags, 1)
        x = x.values.reshape(len(data_batch), lags, 1)

        # get the predictions for the entire batch (batch_size, 1, 1)
        normalised_predictions = self.keras.predict(x)

        # inverse transform the predictions to get the original scale
        predictions = scaler.inverse_transform(normalised_predictions.reshape(-1, 1))

        # reshape to a list of ints and return
        return [int(pred[0]) for pred in predictions]
