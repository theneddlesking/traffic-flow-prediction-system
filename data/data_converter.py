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
    train_normalised_flow = scaler.transform(df_train[target].values.reshape(-1, 1)).reshape(1, -1)[0]
    test_normalised_flow = scaler.transform(df_test[target].values.reshape(-1, 1)).reshape(1, -1)[0]

    train, test = [], []

    for i in range(lags, df_train):
        train.append(train_normalised_flow[i - lags: i + 1])

    for i in range(lags, df_test):
        test.append(test_normalised_flow[i - lags: i + 1])

    train = np.array(train)
    test = np.array(test)
    np.random.shuffle(train)

    x_train = train[:, :-1]
    y_train = train[:, -1]
    x_test = test[:, :-1]
    y_test = test[:, -1]
    y_test_original = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]
    
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    return x_train, y_train, x_test, y_test, y_test_original
