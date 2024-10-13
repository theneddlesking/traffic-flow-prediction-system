import os
import keras
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

    def predict(self, data: list):
        """Predict the output from the input data."""
        return self.keras.predict(data)

    def predict_from_last_n(self, data: list[int], scaler: StandardScaler) -> int:
        """Predict the output from the last n (lags) periods 1D array of flow values as the actual (unnormalised) value."""
        # NOTE: Assuming the input shape is (None, lags, 1), this may need to be changed

        # get lags
        lags = len(data)

        # lags must match the input shape
        if lags != self.keras.input_shape[1]:
            raise ValueError(f"lags must be {self.keras.input_shape[1]}")

        normalised = []

        for i in range(lags):
            normalised.append(
                scaler.transform(
                    [[data[i]]],
                )[
                    0
                ][0],
            )

        # normalised x
        x = [normalised]

        # convert to df
        x = pd.DataFrame(x)

        # reshape to the input shape for model
        x = x.values.reshape(1, lags, 1)

        # get the prediction
        normalised_prediction = self.keras.predict(x)

        # inverse transform
        prediction = scaler.inverse_transform(normalised_prediction)

        # reshape to just int
        prediction = int(prediction[0][0])

        return prediction
