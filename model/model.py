"""
Defination of NN model
"""
import math
import numpy as np
import pandas as pd
import tensorflow as tf
from data.data import process_data
from keras.layers import Dense, Dropout, Activation, LSTM, GRU
from keras.models import Sequential
import sklearn.metrics as metrics
import matplotlib as mpl
import matplotlib.pyplot as plt

HOURS_IN_DAY = 24

MINUTES_IN_HOUR = 60

NUMBER_OF_15_MINUTE_INTERVALS_IN_HOUR = MINUTES_IN_HOUR // 15

# 96 5-minute increments in a day
NUMBER_OF_15_MINUTE_INTERVALS_IN_DAY = (
    HOURS_IN_DAY * NUMBER_OF_15_MINUTE_INTERVALS_IN_HOUR
)


class Model:
    """Model Class
    Build Model.

    # Properties
        model: Model, nn model.
    """

    def __init__(self, location, model_type='gru', units=[12, 64, 64, 1]):
        self.location = location
        self.model_type = model_type
        self.units = units
        self.keras_model = self._get_keras_model()

    def _get_keras_model(self):
        """_get_keras_model
        Get the actual keras model.

        # Returns
            model: Model, nn model.
        """

        if self.model_type == 'lstm':
            model = self.get_lstm(self.units)
        elif self.model_type == 'gru':
            model = self.get_gru(self.units)
        else:
            raise ValueError('Model type not supported')
        # TODO: add saes model type

        return model

    def get_lstm(self, units):
        """LSTM(Long Short-Term Memory)
        Build LSTM Model.

        # Arguments
            units: List(int), number of input, output and hidden units.
        # Returns
            model: Model, nn model.
        """

        # check if units contains at least 3 elements
        if len(units) < 3:
            raise ValueError('units must contain at least 3 elements')

        model = Sequential()
        model.add(LSTM(units[1], input_shape=(units[0], 1), return_sequences=True))

        # loop through units and add layers
        for unit in units[2:-1]:
            model.add(LSTM(unit))
            model.add(Dropout(0.2))
        
        # add output layer
        model.add(Dense(units[-1], activation='sigmoid'))

        return model


    def get_gru(self, units):
        """GRU(Gated Recurrent Unit)
        Build GRU Model.

        # Arguments
            units: List(int), number of input, output and hidden units.
        # Returns
            model: Model, nn model.
        """

        # check if units contains at least 3 elements
        if len(units) < 3:
            raise ValueError('units must contain at least 3 elements')

        model = Sequential()
        model.add(GRU(units[1], input_shape=(units[0], 1), return_sequences=True))

        for unit in units[2:-1]:
            model.add(GRU(unit))
            model.add(Dropout(0.2))
        
        # add output layer
        model.add(Dense(units[-1], activation='sigmoid'))

        return model


    def _get_sae(self, inputs, hidden, output):
        """SAE(Auto-Encoders)
        Build SAE Model.

        # Arguments
            inputs: Integer, number of input units.
            hidden: Integer, number of hidden units.
            output: Integer, number of output units.
        # Returns
            model: Model, nn model.
        """

        model = Sequential()
        model.add(Dense(hidden, input_dim=inputs, name='hidden'))
        model.add(Activation('sigmoid'))
        model.add(Dropout(0.2))
        model.add(Dense(output, activation='sigmoid'))

        return model


    def get_saes(self, layers):
        """SAEs(Stacked Auto-Encoders)
        Build SAEs Model.

        # Arguments
            layers: List(int), number of input, output and hidden units.
        # Returns
            models: List(Model), List of SAE and SAEs.
        """
        # TODO: allow for n number of layers
        sae1 = self._get_sae(layers[0], layers[1], layers[-1])
        sae2 = self._get_sae(layers[1], layers[2], layers[-1])
        sae3 = self._get_sae(layers[2], layers[3], layers[-1])

        saes = Sequential()
        saes.add(Dense(layers[1], input_dim=layers[0], name='hidden1'))
        saes.add(Activation('sigmoid'))
        saes.add(Dense(layers[2], name='hidden2'))
        saes.add(Activation('sigmoid'))
        saes.add(Dense(layers[3], name='hidden3'))
        saes.add(Activation('sigmoid'))
        saes.add(Dropout(0.2))
        saes.add(Dense(layers[4], activation='sigmoid'))

        models = [sae1, sae2, sae3, saes]

        return models
    
    def train(self, x_train, y_train, config, root):
        """train
        Trains a single model on a given location.

        # Arguments
            model: Model, NN model to train.
            x_train: ndarray(number, lags), Input data for train.
            y_train: ndarray(number, ), result data for train.
            name: String, name of model.
            config: Dict, parameter for train.
        """

        self.keras_model.compile(loss="mse", optimizer="rmsprop", metrics=["mape"])
        hist = self.keras_model.fit(
            x_train,
            y_train,
            batch_size=config["batch"],
            epochs=config["epochs"],
            validation_split=0.05,
        )

        self.keras_model.save(root + "/model/vic/" + self.location + "_" + self.model_type + ".keras")
        df = pd.DataFrame.from_dict(hist.history)
        df.to_csv(
            root + "/model/vic/" + self.location + "_" + self.model_type + " loss.csv",
            encoding="utf-8",
            index=False,
        )
    
    def train_for_location(self, root, config):
        """Train the model for a specific location.

        Args:
            location (str): The location to train the model for.
            root (str): The root file path.
            model (str): The model to train.
            config (dict): The configuration for training the model.
        """
        lag = 12

        file1 = root + "/data/vic_test_train/train_" + self.location + ".csv"
        file2 = root + "/data/vic_test_train/test_" + self.location + ".csv"

        print(f"Training model for location: {self.location}")
        print(file1)
        print(file2)

        try:
            with open(file1, encoding="utf-8") as f:
                pass

            with open(file2, encoding="utf-8") as f:
                pass

        except FileNotFoundError:
            print("File not found. Check that you have the correct location name.")
            return

        x_train, y_train, _, _, _ = process_data(file1, file2, lag)

        if self.model_type == "lstm":
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
            self.train(x_train, y_train, config, root)
        if self.model_type == "gru":
            x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))
            self.train(x_train, y_train, config, root)
        # if self.model_type == "saes":
            # x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1]))
            # self.train_saes(x_train, y_train, config, root)

    def MAPE(self, y_true, y_pred):
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


    def eva_regress(self, y_true, y_pred):
        """Evaluation
        Evaluate the predicted result.

        # Arguments
            y_true: List/ndarray, ture data.
            y_pred: List/ndarray, predicted data.
        """

        mape = self.MAPE(y_true, y_pred)
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

    def plot_results(self, y_true, y_preds, names, location):
        """Plot
        Plot the true data and predicted data.

        # Arguments
            y_true: List/ndarray, ture data.
            y_pred: List/ndarray, predicted data.
            names: List, Method names.
        """
        d = "2016-1-1 00:00"
        x = pd.date_range(d, periods=NUMBER_OF_15_MINUTE_INTERVALS_IN_DAY, freq="15min")

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

    def run(self, save_image=True):
        lag = 12
        file1 = "data/vic_test_train/train_" + self.location + ".csv"
        file2 = "data/vic_test_train/test_" + self.location + ".csv"

        _, _, x_test, y_test, scaler = process_data(file1, file2, lag)
        y_test = scaler.inverse_transform(y_test.reshape(-1, 1)).reshape(1, -1)[0]

        y_preds = []
        x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
        predicted = self.keras_model.predict(x_test)
        predicted = scaler.inverse_transform(predicted.reshape(-1, 1)).reshape(1, -1)[0]
        y_preds.append(predicted[:NUMBER_OF_15_MINUTE_INTERVALS_IN_DAY])
        self.eva_regress(y_test, predicted)

        # get predictions for each time interval

        predictions = []

        for i in range(NUMBER_OF_15_MINUTE_INTERVALS_IN_DAY):
            prediction = []
            for y_pred in y_preds:
                prediction.append(y_pred[i])
            predictions.append(prediction)

        if save_image:
            self.plot_results(
                y_test[:NUMBER_OF_15_MINUTE_INTERVALS_IN_DAY], y_preds, self.model_type, self.location
            )

        return predictions
