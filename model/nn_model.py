import os
import keras
from numpy import ndarray
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
