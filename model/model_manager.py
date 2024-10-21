from model.nn_model import Model


class ModelManager:
    """ "General manager for all models in the system"""

    def __init__(self):
        self.models: list[Model] = []

    def add_model(self, model: Model):
        """Add a model to the manager"""
        self.models.append(model)

    def get_model(self, model_name: str) -> Model:
        """Get a model by name"""
        for model in self.models:
            if model.name == model_name:
                return model

        return None
