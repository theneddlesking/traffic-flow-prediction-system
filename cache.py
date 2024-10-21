from db.db_cache import DBCache
from example_data import real_time_source
from models import model_manager


default_cache = DBCache("./db/site.db", [real_time_source], model_manager)
