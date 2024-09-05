"""
Train the NN model.
"""

import sys
import warnings
import argparse
import numpy as np
import pandas as pd
import tensorflow as tf
from data.data import process_data
from model import model
import keras

# as of keras 3.0, the practice has changed to directly accessing models, layers, etc. in code e.g. keras.models.load_model
from keras.callbacks import EarlyStopping

warnings.filterwarnings("ignore")


def train_model(model, X_train, y_train, name, config, root):
    """train
    train a single model.

    # Arguments
        model: Model, NN model to train.
        X_train: ndarray(number, lags), Input data for train.
        y_train: ndarray(number, ), result data for train.
        name: String, name of model.
        config: Dict, parameter for train.
    """

    model.compile(loss="mse", optimizer="rmsprop", metrics=["mape"])
    # early = EarlyStopping(monitor='val_loss', patience=30, verbose=0, mode='auto')
    hist = model.fit(
        X_train,
        y_train,
        batch_size=config["batch"],
        epochs=config["epochs"],
        validation_split=0.05,
    )

    # https://keras.io/guides/migrating_to_keras_3/ - Keras 3 only supports V3 `.keras` files and legacy H5 format files (`.h5` extension)
    # updated to just use .keras extension instead of .h5
    model.save(root + "/model/" + name + ".keras")
    df = pd.DataFrame.from_dict(hist.history)
    df.to_csv(root + "/model/" + name + " loss.csv", encoding="utf-8", index=False)


def train_saes(models, X_train, y_train, name, config, root):
    """train
    train the SAEs model.

    # Arguments
        models: List, list of SAE model.
        X_train: ndarray(number, lags), Input data for train.
        y_train: ndarray(number, ), result data for train.
        name: String, name of model.
        config: Dict, parameter for train.
    """

    temp = X_train
    # early = EarlyStopping(monitor='val_loss', patience=30, verbose=0, mode='auto')

    for i in range(len(models) - 1):
        if i > 0:
            p = models[i - 1]
            # see import statements for more info
            # p.input -> p.inputs
            # new update of tensorflow doesn't require input=/output=
            hidden_layer_model = keras.Model(p.inputs, p.get_layer("hidden").output)
            temp = hidden_layer_model.predict(temp)

        m = models[i]
        m.compile(loss="mse", optimizer="rmsprop", metrics=["mape"])

        m.fit(
            temp,
            y_train,
            batch_size=config["batch"],
            epochs=config["epochs"],
            validation_split=0.05,
        )

        models[i] = m

    saes = models[-1]
    for i in range(len(models) - 1):
        weights = models[i].get_layer("hidden").get_weights()
        saes.get_layer("hidden%d" % (i + 1)).set_weights(weights)
    train_model(saes, X_train, y_train, name, config, root)


def is_colab():
    """Checks if the code is running on Google Colab."""
    try:
        import google.colab

        return True
    except ImportError:
        return False


def main(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument("--model", default="lstm", help="Model to train.")

    # add arg for root file path

    parser.add_argument("--root", default=".", help="Root file path.")

    # add arg for epochs

    parser.add_argument("--epochs", default=600, help="Number of epochs to train.")

    # force epochs not on gpu

    parser.add_argument(
        "--force",
        default=False,
        help="Force number of epochs to a value above 10 if not on GPU.",
    )

    args = parser.parse_args()

    devices = tf.config.list_physical_devices("GPU")

    if devices:
        print(f"GPU is available: {devices}")
    else:
        print("GPU not available")

    running_on_colab = is_colab()

    if running_on_colab:
        print("Running on Google Colab")

        # set root path to ./traffic-flow-prediction-system because of the way Google Colab handles file paths
        args.root = "./traffic-flow-prediction-system"
    else:
        print("Not running on Google Colab")

    lag = 12

    # if not on gpu then reduce the number of epochs

    if not devices and args.epochs > 10 and not args.force:
        # throw warning if not on gpu

        print(
            "Warning: Not running on GPU. Reducing number of epochs to 10. If you want to train for more epochs anyways, use --force True."
        )

        args.epochs = 10

    config = {"batch": 256, "epochs": args.epochs}

    file1 = args.root + "/data/train.csv"
    file2 = args.root + "/data/test.csv"
    x_train, y_train, _, _, _ = process_data(file1, file2, lag)

    if args.model == "lstm":
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        m = model.get_lstm([12, 64, 64, 1])
        train_model(m, x_train, y_train, args.model, config, args.root)
    if args.model == "gru":
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
        m = model.get_gru([12, 64, 64, 1])
        train_model(m, x_train, y_train, args.model, config, args.root)
    if args.model == "saes":
        x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1]))
        m = model.get_saes([12, 400, 400, 400, 1])
        train_saes(m, x_train, y_train, args.model, config, args.root)


if __name__ == "__main__":
    main(sys.argv)
