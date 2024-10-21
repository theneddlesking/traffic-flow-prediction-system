from data_loader import DataLoader
from data_visualiser import DataVisualiser
from model.model_result import ModelResult
from processing_step import ProcessingSteps

from model.nn_model import Model
from model.training_config import TrainingConfig

basic_model = Model.load("./saved_models/basic_model.keras")


y_true = main_input_data.y_test_original

# predict
y_preds = basic_model.predict(main_input_data.x_test, main_input_data.scaler)

# limit to one day
y_true, y_preds = DataLoader.get_example_day(y_true, y_preds, training_config.lags)

print(y_true)

# create flow time df
preds_df = DataLoader.create_flow_time_df(y_preds)

# result
results = [
    ModelResult(basic_model, y_preds),
]

# plot
DataVisualiser.plot_results(results, y_true)

# save plot
DataVisualiser.save_plot("./results/visualisations/basic_model.png")
