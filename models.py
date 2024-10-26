from model.model_manager import ModelManager
from model.nn_model import Model

# TODO add a models table to the database to keep track of them instead

# and then we can have smart init that doesn't overwrite the models table unless the data is missing

# TODO add smart caching so you don't have to pre-process the model
# maybe at least as an option

model_manager = ModelManager()

gru = Model.load("./saved_models/basic_gru_model.keras")

model_manager.add_model(gru)

lstm = Model.load("./saved_models/basic_lstm_model.keras")

model_manager.add_model(lstm)

saes = Model.load("./saved_models/basic_saes_model.keras")

model_manager.add_model(saes)

rnn = Model.load("./saved_models/basic_rnn_model.keras")

model_manager.add_model(rnn)

bi_lstm = Model.load("./saved_models/basic_bidirectional_lstm_model.keras")

model_manager.add_model(bi_lstm)

bi_gru = Model.load("./saved_models/basic_bidirectional_gru_model.keras")

model_manager.add_model(bi_gru)
