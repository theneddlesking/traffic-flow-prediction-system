from model.nn_model import Model


class ModelResult:
    """ModelResult class to store the results of a model run."""

    # NOTE: Maybe should just store the model name?
    def __init__(self, model: Model, hist_df: "pd.DataFrame"):
        self.model = model
        self.hist_df = hist_df
