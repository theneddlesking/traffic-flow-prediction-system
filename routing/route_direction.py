from routing.point import RoutingPoint


class RouteDirection:
    """How the route is going to be followed"""

    def __init__(self, point_a: RoutingPoint, point_b: RoutingPoint):
        self.point_a = point_a
        self.point_b = point_b

        self.is_straight = self.point_a.street_name == self.point_b.street_name

    def get_direction(self) -> str:
        """Get the direction of the route."""
        if self.is_straight:
            return "Go straight"
        else:
            # TODO figure out how to get the actual turn direction

            return f"Turn from {self.point_a.street_name} to {self.point_b.street_name}"

    def as_json(self) -> dict:
        """Convert the RouteDirection to a JSON serializable dictionary."""
        return {
            "point_a": self.point_a.as_json(),
            "point_b": self.point_b.as_json(),
            "is_straight": self.is_straight,
            "direction": self.get_direction(),
        }
