from routing.point import RoutingPoint


class Route:
    """A Route represents a path between two RoutingPoints and the time taken to travel between them."""

    def __init__(self, waypoints: list[RoutingPoint], hours_taken: int):
        self.waypoints = waypoints
        self.hours_taken = hours_taken

    def as_json(self) -> dict:
        """Convert the Route to a JSON serializable dictionary."""
        return {
            "waypoints": [point.as_json() for point in self.waypoints],
            "hours_taken": self.hours_taken,
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Route):
            return NotImplemented

        # check if scats match
        self_scats = set()

        for point in self.waypoints:
            self_scats.add(point.site_number)

        other_scats = set()

        for point in other.waypoints:
            other_scats.add(point.site_number)

        return self_scats == other_scats
