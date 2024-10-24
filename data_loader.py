from typing import Callable
import numpy as np
import pandas as pd
import os

from sklearn.preprocessing import MinMaxScaler

from model.model_input_data import ModelInputData
from model.real_time_source import RealTimeSource
from time_utils import TimeUtils


class DataLoader:
    """Data Loader class."""

    def __init__(
        self,
        csv_path: str,
        target: str,
        pre_processing_steps: list[Callable[[pd.DataFrame], pd.DataFrame]],
    ):
        self.csv_path = csv_path
        self.target = target
        self.pre_processing_steps = pre_processing_steps

        self.pre_processed_df = self.preprocess_df()

        if not self.df_contains_target():
            raise ValueError(
                "Target column not found in data frame. Make sure the target column is in the data frame after preprocessing."
            )

    def get_df(self) -> pd.DataFrame:
        """Loads data frame from CSV file."""
        return pd.read_csv(self.csv_path, encoding="utf-8")

    def save_df(self, df: pd.DataFrame, new_path: str) -> None:
        """Saves data frame to CSV file."""
        df.to_csv(new_path, encoding="utf-8", index=False)

    def preprocess_df(self) -> pd.DataFrame:
        """Preprocesses the data frame."""
        df = self.get_df()

        for step in self.pre_processing_steps:
            df = step(df)

        return df

    def df_contains_target(self) -> bool:
        """Checks if the target column is in the data frame."""
        return self.target in self.pre_processed_df.columns

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

    def create_train_test_split_from_df(
        self, train_test_proportion: float, lags: int, heuristic_columns: list = None
    ) -> ModelInputData:
        """
        Convert DataFrame to numpy

        # Arguments
            df: DataFrame, data.
            train_test_proportion: float, proportion of data to use for training.
            target: string, target column.
            lags: integer, time lag.
            heuristic_columns: list, list of columns to use as heuristics.
        # Returns
            x_train: ndarray.
            y_train: ndarray.
            x_test: ndarray.
            y_test: ndarray.
            y_test_original: ndarray.
            scaler: StandardScaler.
        """

        df = self.pre_processed_df
        target = self.target

        # split df based on test train proportion but evenly per day

        periods_per_day = 96
        split = int(len(df) / periods_per_day * train_test_proportion) * periods_per_day

        # split df based on test train proportion
        df_train, df_test = (
            df[:split],
            df[split:],
        )

        vals = df[target].values.reshape(-1, 1)

        print(f"vals shape: {vals.shape}")

        # normalise traffic flow
        scaler = MinMaxScaler(feature_range=(0, 1)).fit(df[target].values.reshape(-1, 1))
        train_normalised_flow = scaler.transform(df_train[target].values.reshape(-1, 1)).reshape(1, -1)[0]
        test_normalised_flow = scaler.transform(df_test[target].values.reshape(-1, 1)).reshape(1, -1)[0]

        # normalise heuristics
        if heuristic_columns:
            heuristic_scaler = MinMaxScaler(feature_range=(0, 1)).fit(df[heuristic_columns])
            train_normalised_heuristics = heuristic_scaler.transform(df_train[heuristic_columns])
            test_normalised_heuristics = heuristic_scaler.transform(df_test[heuristic_columns])
        else:
            train_normalised_heuristics = np.zeros((len(df_train), 0))
            test_normalised_heuristics = np.zeros((len(df_test), 0))

        # TODO retain other columns for evaluation

        train, test = [], []
        train_heuristics, test_heuristics = [], []

        for i in range(lags, len(train_normalised_flow)):
            train.append(train_normalised_flow[i - lags : i + 1])
            train_heuristics.append(train_normalised_heuristics[i])
        
        for i in range(lags, len(test_normalised_flow)):
            test.append(test_normalised_flow[i - lags : i + 1])
            test_heuristics.append(test_normalised_heuristics[i])

        train = np.array(train)
        test = np.array(test)
        train_heuristics = np.array(train_heuristics)
        test_heuristics = np.array(test_heuristics)

        # shuffle the training data
        np.random.shuffle(train)

        x_train = train[:, :-1]
        y_train = train[:, -1]
        x_test = test[:, :-1]
        y_test = test[:, -1]
        y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(
            1, -1
        )[0]

        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

        x_train_combined = [x_train, train_heuristics]
        x_test_combined = [x_test, test_heuristics]

        # NOTE: not sure if we need y_test_original or scaler or both
        return ModelInputData(x_train_combined, y_train, x_test_combined, y_test, y_test_original, scaler)

    @staticmethod
    def get_example_day(
        y_true: np.ndarray, y_preds: np.ndarray, lags: int, minutes_in_period: int = 15
    ) -> tuple[np.ndarray, np.ndarray]:
        """Get an example day of true and predicted values."""

        periods_per_day = 24 * 60 // minutes_in_period

        y_true = y_true[periods_per_day - lags : periods_per_day * 2 - lags]
        y_preds = y_preds[periods_per_day - lags : periods_per_day * 2 - lags]

        return y_true, y_preds

    @staticmethod
    def create_flow_time_df(
        y_values: list, minutes_in_period: int = 15
    ) -> pd.DataFrame:
        """Create a time data frame from a day of flow values."""

        # check y_preds is a list with len for number of periods
        number_of_periods = 24 * 60 // minutes_in_period

        if len(y_values) != number_of_periods:
            raise ValueError(f"y_preds must have {number_of_periods} values")

        # create a list of dictionaries
        output_df_rows = []

        for i in range(0, number_of_periods, 1):

            output_df_rows.append(
                {
                    "time": TimeUtils.convert_minute_index_to_str(i, minutes_in_period),
                    "flow": y_values[i],
                },
            )

        return pd.DataFrame(output_df_rows)

    @staticmethod
    def peek(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
        """Peek at the first n rows of a data frame."""
        return df.head(n)

    @staticmethod
    def get_real_time_sources(
        df: pd.DataFrame, lags: int, minutes_per_period: int
    ) -> list[RealTimeSource]:
        # group by location

        grouped = df.groupby("location")

        real_time_sources = []

        location_id = 0

        for name, group in grouped:
            location_id += 1

            day_before = group.iloc[0]
            day_of = group.iloc[1]

            # combine V00 to V95
            day_before_flow = day_before["V00":"V95"].values

            # get first 12
            day_before_flow = day_before_flow[:lags]

            # get flow for the day
            day_of_flow = day_of["V00":"V95"].values

            # create real time source
            real_time_source = RealTimeSource(
                day_of_flow, day_before_flow, location_id, name
            )

            real_time_sources.append(real_time_source)

        return real_time_sources

    @staticmethod
    def load_from_real_time_source(
        real_time_data: RealTimeSource, time_index: int
    ) -> np.ndarray:
        """Load data from a real time source."""

        example_flow_set = real_time_data.get_lag_input_data_for_time(time_index)

        scaler = MinMaxScaler(feature_range=(0, 1)).fit(
            np.array(example_flow_set).reshape(-1, 1)
        )

        example_flow_set = np.array(example_flow_set)

        # TODO consider heuristics later

        return example_flow_set, scaler
