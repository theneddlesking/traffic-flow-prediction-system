# keeping this for now to check over when we implement saes later
def train_saes(models, x_train, y_train, name, config, root, location):
    """train
    train the SAEs model.

    # Arguments
        models: List, list of SAE model.
        x_train: ndarray(number, lags), Input data for train.
        y_train: ndarray(number, ), result data for train.
        name: String, name of model.
        config: Dict, parameter for train.
    """

    temp = x_train
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

    train_model(saes, x_train, y_train, name, config, root, location)
