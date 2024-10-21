from model.nn_model import Model


class ModelResult:
    """ModelResult class to store the results of a model run."""

    def __init__(self, model: Model, y_preds: list):
        self.model = model
        self.y_preds = y_preds
