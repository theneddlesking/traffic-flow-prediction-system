from keras.layers import Dense, Dropout, SimpleRNN, LSTM, GRU, Input
from keras.models import Sequential
from tensorflow.keras import layers, models, regularizers


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
    def get_saes(units: list):
        def build_encoder(input_dim, hidden_units):
            encoder_input = layers.Input(shape=(input_dim,))
            x = encoder_input
            for units in hidden_units[:-1]:
                x = layers.Dense(units, activation='relu', activity_regularizer=regularizers.l1(10e-5))(x)
            encoded_output = layers.Dense(hidden_units[-1], activation='relu')(x)
            return models.Model(encoder_input, encoded_output, name="encoder")

        def build_decoder(hidden_units):
            decoder_input = layers.Input(shape=(hidden_units[-1],))
            x = decoder_input
            for units in hidden_units[::-1][1:]:
                x = layers.Dense(units, activation='relu')(x)
            decoder_output = layers.Dense(1, activation='linear')(x)
            return models.Model(decoder_input, decoder_output, name="decoder")

        def build_autoencoder(input_dim, hidden_units):
            encoder = build_encoder(input_dim, hidden_units)
            decoder = build_decoder(hidden_units)

            autoencoder_input = layers.Input(shape=(input_dim,))
            encoded = encoder(autoencoder_input)
            decoded = decoder(encoded)

            autoencoder = models.Model(autoencoder_input, decoded, name="autoencoder")
            autoencoder.compile(optimizer='adam', loss='mse')

            return autoencoder, encoder, decoder

        input_dim = units[0]
        hidden_units = units[1:]

        return build_autoencoder(input_dim, hidden_units)[0]
    
    @staticmethod
    def get_rnn(units):
        """RNN(Recurrent Neural Network)
        Build RNN Model.

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
        model.add(SimpleRNN(units[1], activation='relu', return_sequences=True, input_shape=(units[0], 1)))

        # additional RNN layers with dropout
        for unit in units[2:-1]:
            model.add(SimpleRNN(unit, activation='relu', return_sequences=True))
            model.add(Dropout(0.2))

        # add output layer
        model.add(SimpleRNN(units[-2], activation='relu'))

        model.add(Dense(units[-1]))
        model.compile(optimizer='adam', loss='mse')
        
        return model
