from routing.direction import Direction


class RoutingPoint:
    """An intersection point is a point where two streets intersect. The first street name is the name of the street the location is on."""

    def __init__(
        self,
        location_id: int,
        site_number: int,
        lat: float,
        long: float,
        direction: str,
        street_name: str,
        other_street_name: str,
    ):
        self.location_id = location_id
        self.site_number = site_number
        self.lat = lat
        self.long = long
        self.direction = Direction(direction)
        self.street_name = street_name
        self.other_street_name = other_street_name

        self.street_names = set([street_name, other_street_name])

    @classmethod
    def from_raw_location_data(cls, location: dict):
        """Create a routing point from raw location data."""
        location_name = location["name"]
        lat = location["lat"]
        long = location["long"]
        site_number = location["site_number"]

        street_name, other_street_name = (
            cls.get_intersection_street_names_from_location_name(location_name)
        )

        direction = cls.get_direction_from_location_name(location_name)

        return cls(
            location_id=location["location_id"],
            site_number=site_number,
            lat=lat,
            long=long,
            direction=direction,
            street_name=street_name,
            other_street_name=other_street_name,
        )

    @staticmethod
    def get_intersection_street_names_from_location_name(
        location_name: str,
    ) -> list[str]:
        """From location name returns the street names that intersect at that location. /
        The first street name is the name of the street the location is on."""
        words = location_name.split(" ")

        street_name_separators = ["_", "."]

        streets = [
            word
            for word in words
            if any(separator in word for separator in street_name_separators)
        ]

        return streets

    @staticmethod
    def get_direction_from_location_name(location_name: str) -> str:
        """Get the direction from a location name."""
        cardinal_directions = ["N", "S", "E", "W"]

        inter_cardinal_directions = ["NE", "NW", "SE", "SW"]

        all_directions = cardinal_directions + inter_cardinal_directions

        words = location_name.split(" ")

        for word in words:
            if word in all_directions:
                return word

        return None

    def __eq__(self, other):
        return self.location_id == other.location_id

    def __hash__(self):
        return self.location_id
