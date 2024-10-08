import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


def convert_csv_to_df(csv):
    """
    Convert CSV data to a DataFrame
    """
    return pd.read_csv(csv, encoding="utf-8")

def create_train_test_split_from_df(df, train_test_proportion, target, lags):
    """
    Convert DataFrame to numpy

    # Arguments
        df: DataFrame, data.
        lags: integer, time lag.
    # Returns
        x_train: ndarray.
        y_train: ndarray.
        x_test: ndarray.
        y_test: ndarray.
        scaler: StandardScaler.
    """

    # split df based on test train proportion
    df_train, df_test = df[:int(len(df) * train_test_proportion)], df[int(len(df) * train_test_proportion):]

    scaler = MinMaxScaler(feature_range=(0, 1)).fit(df[target].values.reshape(-1, 1))
    normalised_flow = scaler.transform(df_train[target].values.reshape(-1, 1)).reshape(1, -1)[0]
    normalised_flow = scaler.transform(df_test[target].values.reshape(-1, 1)).reshape(1, -1)[0]

    train, test = [], []

    for i in range(lags, df_train):
        train.append(normalised_flow[i - lags: i + 1])

    for i in range(lags, df_test):
        test.append(normalised_flow[i - lags: i + 1])

    train = np.array(train)
    test = np.array(test)
    np.random.shuffle(train)

    X_train = train[:, :-1]
    y_train = train[:, -1]
    X_test = test[:, :-1]
    y_test = test[:, -1]

    return df[target].values
