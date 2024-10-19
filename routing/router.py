from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
from routing.route import Route


class Router:
    """A router is a tool to find the shortest path between two RoutingPoints in a given RoadNetwork."""

    async def find_route(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_of_day: str,
        network: RoadNetwork,
    ) -> Route:
        """Find the shortest route between two RoutingPoints and time taken in hours."""
        raise NotImplementedError("find_route method must be implemented by subclass.")

    async def find_best_routes(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_of_day: str,
        network: RoadNetwork,
    ) -> list[Route]:
        """Find the best routes between two points."""
        raise NotImplementedError(
            "find_best_routes method must be implemented by subclass."
        )
