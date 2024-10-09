from db.instance import db

# copy predictions into basic_predictions

db.copy_table("predictions", "basic_predictions")

# drop predictions

db.drop_table("predictions")
