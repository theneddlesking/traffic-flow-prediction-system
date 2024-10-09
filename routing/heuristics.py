from routing.point import RoutingPoint


class Heuristics:
    """A collection of heuristic functions for use in the A* algorithm."""

    @staticmethod
    def no_heuristic(point1: RoutingPoint, point2: RoutingPoint) -> int:
        return 0
