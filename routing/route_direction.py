from routing.point import RoutingPoint


class RouteDirection:
    """How the route is going to be followed"""

    def __init__(self, point_a: RoutingPoint, point_b: RoutingPoint):
        self.point_a = point_a
        self.point_b = point_b

        self.is_straight = self.point_a.street_name == self.point_b.street_name

        self.distance_km = self.point_a.distance_to(self.point_b)

    def get_distance_str(self) -> str:
        """Get the distance of the route as a string."""
        # nicely format distance eg. "300m", or "1.2km"

        # nearest
        nearest = 50

        # closer to 1km
        closer_to_1km = 1 - nearest / 1000

        if self.distance_km < closer_to_1km:
            # convert to meters
            meters = self.distance_km * 1000

            # round to nearest 50m
            rounded_meters = round(meters / nearest) * nearest

            return f"{rounded_meters}m"

        # round to nearest 100m
        rounded_km = round(self.distance_km * 10) / 10

        # convert 1.0 to 1
        if rounded_km.is_integer():
            rounded_km = int(rounded_km)

        return f"{rounded_km}km"

    def get_direction(self, next_direction: "RouteDirection") -> str:
        """Get the direction of the route."""

        destination = f"{self.point_b.street_name}/{self.point_b.other_street_name}"

        if self.is_straight:
            straight_str = f"Go straight along {self.point_a.street_name} for {self.get_distance_str()}"

            # if next direction is straight we can specify we have passed an intersection
            if next_direction and next_direction.is_straight:
                return f"{straight_str} and continuing through the intersection at {self.point_b.other_street_name}"
            if next_direction:
                return straight_str

            return f"{straight_str} for {self.get_distance_str()} to arrive at your destination at {destination}"
        else:
            # TODO figure out how to get the actual turn direction

            turn_str = (
                f"Turn from {self.point_a.street_name} to {self.point_b.street_name}"
            )

            if next_direction:
                return turn_str

            return f"{turn_str} to arrive at your destination at {destination}"

    def as_json(self, next_direction: "RouteDirection") -> dict:
        """Convert the RouteDirection to a JSON serializable dictionary."""
        return {
            "instruction": self.get_direction(next_direction),
            "distance": self.get_distance_str(),
            "is_straight": self.is_straight,
        }

    def get_turn(self) -> str:
        """Get the simplified turn string of the route."""
        return f"{self.point_a.street_name} to {self.point_b.street_name}"
