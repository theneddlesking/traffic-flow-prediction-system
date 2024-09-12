"""
Traffic Flow Prediction with Neural Networks(SAEs、LSTM、GRU).
"""

import math
import warnings
import numpy as np
import pandas as pd
from data.data import process_data
import keras

# as of keras 3.0, the practice has changed to directly accessing models, layers, etc. in code e.g. keras.models.load_model
import sklearn.metrics as metrics
import matplotlib as mpl
import matplotlib.pyplot as plt

import argparse

warnings.filterwarnings("ignore")

HOURS_IN_DAY = 24

MINUTES_IN_HOUR = 60

NUMBER_OF_5_MINUTE_INTERVALS_IN_HOUR = MINUTES_IN_HOUR // 5

# 288 5-minute increments in a day
NUMBER_OF_5_MINUTE_INTERVALS_IN_DAY = (
    HOURS_IN_DAY * NUMBER_OF_5_MINUTE_INTERVALS_IN_HOUR
)


def MAPE(y_true, y_pred):
    """Mean Absolute Percentage Error
    Calculate the mape.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
    # Returns
        mape: Double, result data for train.
    """

    y = [x for x in y_true if x > 0]
    y_pred = [y_pred[i] for i in range(len(y_true)) if y_true[i] > 0]

    num = len(y_pred)
    sums = 0

    for i in range(num):
        tmp = abs(y[i] - y_pred[i]) / y[i]
        sums += tmp

    mape = sums * (100 / num)

    return mape


def eva_regress(y_true, y_pred):
    """Evaluation
    evaluate the predicted resul.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
    """

    mape = MAPE(y_true, y_pred)
    vs = metrics.explained_variance_score(y_true, y_pred)
    mae = metrics.mean_absolute_error(y_true, y_pred)
    mse = metrics.mean_squared_error(y_true, y_pred)
    r2 = metrics.r2_score(y_true, y_pred)
    print("explained_variance_score:%f" % vs)
    print("mape:%f%%" % mape)
    print("mae:%f" % mae)
    print("mse:%f" % mse)
    print("rmse:%f" % math.sqrt(mse))
    print("r2:%f" % r2)


def plot_results(y_true, y_preds, names, location):
    """Plot
    Plot the true data and predicted data.

    # Arguments
        y_true: List/ndarray, ture data.
        y_pred: List/ndarray, predicted data.
        names: List, Method names.
    """
    d = "2016-3-4 00:00"
    x = pd.date_range(d, periods=288, freq="5min")

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.plot(x, y_true, label="True Data")
    for name, y_pred in zip(names, y_preds):
        ax.plot(x, y_pred, label=name)

    plt.legend()
    plt.grid(True)
    plt.xlabel("Time of Day")
    plt.ylabel("Flow")

    date_format = mpl.dates.DateFormatter("%H:%M")
    ax.xaxis.set_major_formatter(date_format)
    fig.autofmt_xdate()

    # save plot
    plt.savefig("images/vic/" + location + ".png")


def run_model(location, model_names, save_image=True):

    if model_names is None:
        model_names = ["lstms", "grus", "saes"]

    lag = 12
    file1 = "data/vic_test_train/train_" + location + ".csv"
    file2 = "data/vic_test_train/test_" + location + ".csv"

    _, _, X_test, y_test, scaler = process_data(file1, file2, lag)
    y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]

    models = []

    # see import statements for more info
    for name in model_names:
        models.append(
            keras.models.load_model(
                "model/vic/" + location + "_" + name.lower() + ".keras"
            )
        )

    y_preds = []
    for name, model in zip(model_names, models):
        if name == "saes":
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1]))
        else:
            X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))
        # "this is a bug of Keras" - https://github.com/XifengGuo/CapsNet-Keras/issues/7
        # file = 'images/' + name + '.png'
        # keras.utils.plot_model(model, to_file=file, show_shapes=True)
        predicted = model.predict(X_test)
        predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]
        y_preds.append(predicted[:NUMBER_OF_5_MINUTE_INTERVALS_IN_DAY])
        print(name)
        eva_regress(y_test, predicted)

    # get predictions for each time interval

    predictions = []

    for i in range(NUMBER_OF_5_MINUTE_INTERVALS_IN_DAY):
        prediction = []
        for y_pred in y_preds:
            prediction.append(y_pred[i])
        predictions.append(prediction)

    if save_image:
        plot_results(
            y_test[:NUMBER_OF_5_MINUTE_INTERVALS_IN_DAY], y_preds, model_names, location
        )

    return predictions


def main():
    parser = argparse.ArgumentParser()

    # add arg for location
    parser.add_argument(
        "--location",
        help="Location to extract data from.",
    )

    # add arg for models

    parser.add_argument(
        "--models",
        nargs="+",
        help="Models to train.",
    )

    args = parser.parse_args()

    location = args.location

    models = args.models

    # verify location

    if location is None:
        raise ValueError("Location is required")

    # verify models

    if models is None:
        raise ValueError("Models are required")

    models = [model.lower() for model in models]

    valid_models = ["lstm", "gru", "saes"]

    for model in models:
        if model not in valid_models:
            raise ValueError(f"Invalid model {model}. Valid models are {valid_models}")

    run_model(location, models)


if __name__ == "__main__":
    main()
