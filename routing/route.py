from routing.point import RoutingPoint
from routing.route_direction import RouteDirection


class Route:
    """A Route represents a path between two RoutingPoints and the time taken to travel between them."""

    def __init__(self, waypoints: list[RoutingPoint], hours_taken: int):
        self.waypoints = waypoints
        self.hours_taken = hours_taken

        self.directions: list[RouteDirection] = []

        for i in range(len(waypoints) - 1):
            self.directions.append(RouteDirection(waypoints[i], waypoints[i + 1]))

    def as_json(self) -> dict:
        """Convert the Route to a JSON serializable dictionary."""

        # convert to object as { "instruction " : Direction}

        return {
            "waypoints": [point.as_json() for point in self.waypoints],
            "hours_taken": self.hours_taken,
            "directions": [
                (
                    direction.as_json(self.directions[i + 1])
                    if i + 1 < len(self.directions)
                    else direction.as_json(None)
                )
                for i, direction in enumerate(self.directions)
            ],
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

        if self_scats == other_scats:
            return True

        # check if we have just gone through the same path
        # eg. different directions but same path

        def get_sequence_of_turns(directions: list[RouteDirection]) -> list[str]:
            """Get a sequence of turns from a list of RouteDirections."""
            turns = [
                direction.get_turn()
                for direction in directions
                if not direction.is_straight
            ]

            return turns

        self_turns = get_sequence_of_turns(self.directions)
        other_turns = get_sequence_of_turns(other.directions)

        return self_turns == other_turns

    def __str__(self) -> str:
        return f"Route: {self.waypoints}, {self.hours_taken} hours"

    def __repr__(self) -> str:
        return self.__str__()
