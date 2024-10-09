from db.sqlite_db import DBModel


class Controller:
    """Controller class"""

    def __init__(self, model: DBModel):
        self.model = model
