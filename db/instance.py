# init db
from db.flow_controller import FlowController
from db.flow_model import FlowPredictorModel
from db.site_controller import SiteController
from db.site_model import SiteModel
from db.spoofed_model import SpoofedModel
from db.sqlite_db import SQLiteDB


db = SQLiteDB("./db/site.db")

site_model = SiteModel(db)

site_controller = SiteController(site_model)

flow_model = FlowPredictorModel(db, SpoofedModel("basic"))

basic_flow_controller = FlowController(flow_model)
