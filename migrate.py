from cache import default_cache

# copy predictions into basic_predictions

default_cache.db.copy_table("basic_model_predictions", "basic_gru_model_predictions")

# drop predictions

default_cache.db.drop_table("basic_model_predictions")
