from model.model_manager import ModelManager
from model.nn_model import Model


model_manager = ModelManager()

basic_model = Model.load("./saved_models/basic_model.keras")

model_manager.add_model(basic_model)
