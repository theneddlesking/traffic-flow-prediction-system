from routing.point import RoutingPoint
from routing.road_network import RoadNetwork


class Router:
    """A router is a tool to find the shortest path between two RoutingPoints in a given RoadNetwork."""

    def find_route(
        self, start: RoutingPoint, end: RoutingPoint, network: RoadNetwork
    ) -> list[RoutingPoint]:
        """Find the shortest route between two RoutingPoints."""
        raise NotImplementedError("find_route method must be implemented by subclass.")
