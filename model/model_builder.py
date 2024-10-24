from keras.layers import Dense, Dropout, Activation, LSTM, GRU, Input
from keras.models import Sequential


class ModelBuilder:
    """Returns a Keras model based on the model type"""

    @staticmethod
    def get_lstm(units: list):
        """LSTM(Long Short-Term Memory)
        Build LSTM Model.

        # Arguments
            units: List(int), number of input, output and hidden units.
        # Returns
            model: Model, nn model.
        """

        # check if units contains at least 3 elements
        if len(units) < 3:
            raise ValueError("units must contain at least 3 elements")

        model = Sequential()

        # add input layer
        model.add(Input(shape=(units[0], 1)))

        model.add(LSTM(units[1], return_sequences=True))

        # loop through units and add layers
        for unit in units[2:-1]:
            model.add(LSTM(unit))
            model.add(Dropout(0.2))

        # add output layer
        model.add(Dense(units[-1], activation="sigmoid"))

        return model

    @staticmethod
    def get_gru(units: list):
        """GRU(Gated Recurrent Unit)
        Build GRU Model.

        # Arguments
            units: List(int), number of input, output and hidden units.
        # Returns
            model: Model, nn model.
        """

        # check if units contains at least 3 elements
        if len(units) < 3:
            raise ValueError("units must contain at least 3 elements")

        model = Sequential()

        # add input layer
        model.add(Input(shape=(units[0], 1)))

        model.add(GRU(units[1], return_sequences=True))

        for unit in units[2:-1]:
            model.add(GRU(unit))
            model.add(Dropout(0.2))

        # add output layer
        model.add(Dense(units[-1], activation="sigmoid"))

        return model

    @staticmethod
    def _get_sae(inputs: int, hidden: int, output: int):
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
        model.add(Dense(hidden, input_dim=inputs, name="hidden"))
        model.add(Activation("sigmoid"))
        model.add(Dropout(0.2))
        model.add(Dense(output, activation="sigmoid"))

        return model

    # TODO implement a more conventional way of building SAEs
    @staticmethod
    def get_saes(layers: list):
        """SAEs(Stacked Auto-Encoders)
        Build SAEs Model.

        # Arguments
            layers: List(int), number of input, output and hidden units.
        # Returns
            models: List(Model), List of SAE and SAEs.
        """
        # TODO: allow for n number of layers

        sae1 = ModelBuilder._get_sae(layers[0], layers[1], layers[-1])
        sae2 = ModelBuilder._get_sae(layers[1], layers[2], layers[-1])
        sae3 = ModelBuilder._get_sae(layers[2], layers[3], layers[-1])

        saes = Sequential()
        saes.add(Dense(layers[1], input_dim=layers[0], name="hidden1"))
        saes.add(Activation("sigmoid"))
        saes.add(Dense(layers[2], name="hidden2"))
        saes.add(Activation("sigmoid"))
        saes.add(Dense(layers[3], name="hidden3"))
        saes.add(Activation("sigmoid"))
        saes.add(Dropout(0.2))
        saes.add(Dense(layers[4], activation="sigmoid"))

        models = [sae1, sae2, sae3, saes]

        return models
