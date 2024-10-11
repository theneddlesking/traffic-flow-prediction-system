from typing import Callable
import numpy as np
import pandas as pd
import os

from sklearn.preprocessing import MinMaxScaler

from model_input_data import ModelInputData


class DataLoader:
    """Loads data frame from CSV file and processes it."""

    def __init__(
        self,
        csv_path: str,
        target: str,
        pre_processing_steps: list[Callable[[pd.DataFrame], pd.DataFrame]],
    ):
        self.csv_path = csv_path
        self.target = target
        self.pre_processing_steps = pre_processing_steps

    def get_df(self) -> pd.DataFrame:
        """Loads data frame from CSV file."""
        return pd.read_csv(self.csv_path, encoding="utf-8")

    def save_df(self, df: pd.DataFrame, new_path: str) -> None:
        """Saves data frame to CSV file."""
        df.to_csv(new_path, encoding="utf-8", index=False)

    def preprocess_df(self, df: pd.DataFrame) -> pd.DataFrame:
        """Preprocesses the data frame."""
        for step in self.pre_processing_steps:
            df = step(df)

        return df

    def df_contains_target(self, df: pd.DataFrame) -> bool:
        """Checks if the target column is in the data frame."""
        return self.target in df.columns

    # TODO should these static methods be in a separate class?

    @staticmethod
    def clear_directory(directory: str) -> None:
        """Clears the directory of all files."""

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
            except FileNotFoundError as e:
                print(f"Error removing {file_path}: {e}")

    # NOTE: Not sure this is the best spot for this method
    @staticmethod
    def is_colab():
        """Checks if the code is running on Google Colab."""
        try:
            import google.colab  # noqa, pylint: disable=all, type: ignore

            return True
        except ImportError:
            return False

    # TODO remove ref to models in comments
    @staticmethod
    def expand_to_3D(x_train: np.ndarray) -> np.ndarray:
        """Expands the dimensions of the input data to 3D. (For LSTM and GRU models?)"""
        return x_train.reshape(x_train.shape[0], x_train.shape[1], 1)

    @staticmethod
    def collapse_to_2D(x_train: np.ndarray) -> np.ndarray:
        """Collapses the dimensions of the input data to 2D. (For SAES models?)"""
        return x_train.reshape(x_train.shape[0], x_train.shape[1])

    @staticmethod
    def create_train_test_split_from_df(
        df: pd.DataFrame, train_test_proportion: float, target: str, lags: int
    ) -> ModelInputData:
        """
        Convert DataFrame to numpy

        # Arguments
            df: DataFrame, data.
            train_test_proportion: float, proportion of data to use for training.
            target: string, target column.
            lags: integer, time lag.
        # Returns
            x_train: ndarray.
            y_train: ndarray.
            x_test: ndarray.
            y_test: ndarray.
            y_test_original: ndarray.
            scaler: StandardScaler.
        """

        # split df based on test train proportion but evenly per day

        periods_per_day = 96

        split = int(len(df) / periods_per_day * train_test_proportion) * periods_per_day

        print(f"Splitting data at {split}")

        # split df based on test train proportion
        df_train, df_test = (
            df[:split],
            df[split:],
        )

        # save as csv

        df_train.to_csv("train.csv", index=False)
        df_test.to_csv("test.csv", index=False)

        scaler = MinMaxScaler(feature_range=(0, 1)).fit(
            df[target].values.reshape(-1, 1)
        )
        train_normalised_flow = scaler.transform(
            df_train[target].values.reshape(-1, 1)
        ).reshape(1, -1)[0]
        test_normalised_flow = scaler.transform(
            df_test[target].values.reshape(-1, 1)
        ).reshape(1, -1)[0]

        train, test = [], []

        for i in range(lags, len(train_normalised_flow)):
            train.append(train_normalised_flow[i - lags : i + 1])
        for i in range(lags, len(test_normalised_flow)):
            test.append(test_normalised_flow[i - lags : i + 1])

        train = np.array(train)
        test = np.array(test)

        # shuffle the training data
        np.random.shuffle(train)

        x_train = train[:, :-1]
        y_train = train[:, -1]
        x_test = test[:, :-1]
        y_test = test[:, -1]
        y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(
            1, -1
        )[0]

        # NOTE: reshaping for LSTM, might be different for SAES or other models

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        # NOTE: not sure if we need y_test_original or scaler or both
        return ModelInputData(x_train, y_train, x_test, y_test, y_test_original, scaler)
