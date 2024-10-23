import numpy as np
from sklearn.preprocessing import StandardScaler


class ModelInputData:
    """Defines the data that will be used to train and test the model."""

    def __init__(
        self,
        x_train: np.ndarray,
        y_train: np.ndarray,
        x_test: np.ndarray,
        y_test: np.ndarray,
        y_test_original: np.ndarray,
        scaler: StandardScaler,
    ):
        self.x_train = x_train
        self.y_train = y_train
        self.x_test = x_test
        self.y_test = y_test
        self.y_test_original = y_test_original
        self.scaler = scaler
