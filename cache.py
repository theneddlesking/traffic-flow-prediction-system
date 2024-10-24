from db.db_cache import DBCache
from models import model_manager
from sources import sources


default_cache = DBCache("./db/site.db", sources, model_manager)
