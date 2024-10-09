class Location:
    """A location in a road network."""

    def __init__(
        self,
        location_id: int,
        site_number: int,
        name: str,
        lat: float,
        long: float,
    ):
        self.name = name
        self.location_id = location_id
        self.site_number = site_number
        self.lat = lat
        self.long = long
