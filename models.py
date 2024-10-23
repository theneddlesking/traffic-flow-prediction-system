from model.model_manager import ModelManager
from model.nn_model import Model

# TODO add a models table to the database to keep track of them instead

# and then we can have smart init that doesn't overwrite the models table unless the data is missing

# TODO add smart caching so you don't have to pre-process the model
# maybe at least as an option

model_manager = ModelManager()

basic_model = Model.load("./saved_models/basic_model.keras")

model_manager.add_model(basic_model)

lstm = Model.load("./saved_models/basic_lstm_model.keras")

model_manager.add_model(lstm)
