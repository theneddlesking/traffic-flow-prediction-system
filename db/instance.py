# init db
from db.flow_controller import FlowController
from db.flow_model import FlowPredictorModel
from db.site_controller import SiteController
from db.site_model import SiteModel
from db.sqlite_db import SQLiteDB
from model.real_time_source import RealTimeSource


db = SQLiteDB("./db/site.db")

site_model = SiteModel(db)

site_controller = SiteController(site_model)

# TODO fix this, TEMPORARY !
actual_data = [
    32,
    30,
    20,
    19,
    16,
    25,
    10,
    9,
    6,
    6,
    6,
    12,
    6,
    12,
    11,
    7,
    8,
    4,
    10,
    7,
    10,
    12,
    20,
    23,
    28,
    41,
    46,
    53,
    53,
    43,
    59,
    75,
    100,
    103,
    125,
    141,
    148,
    175,
    168,
    152,
    190,
    170,
    157,
    204,
    164,
    179,
    164,
    223,
    185,
    156,
    252,
    148,
    163,
    173,
    174,
    149,
    151,
    176,
    130,
    159,
    172,
    144,
    136,
    161,
    145,
    161,
    160,
    186,
    160,
    147,
    160,
    172,
    162,
    150,
    151,
    150,
    123,
    112,
    111,
    98,
    71,
    70,
    67,
    53,
    68,
    62,
    64,
    37,
    40,
    54,
    36,
    45,
    44,
    37,
    46,
    34,
]


flow_model = FlowPredictorModel(db, RealTimeSource())

basic_flow_controller = FlowController(flow_model)
