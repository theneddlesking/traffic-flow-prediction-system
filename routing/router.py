from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
from routing.route import Route
from routing.time_estimator import TimeEstimator


class Router:
    """A router is a tool to find the shortest path between two RoutingPoints in a given RoadNetwork."""

    def __init__(self, time_estimator: TimeEstimator):
        self.time_estimator = time_estimator

    async def find_route(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_of_day: str,
        network: RoadNetwork,
    ) -> Route:
        """Find the shortest route between two RoutingPoints and time taken in hours."""
        raise NotImplementedError("find_route method must be implemented by subclass.")

    async def create_graph(
        self,
        time_of_day: int,
        road_network: RoadNetwork,
    ) -> dict[int, dict[int, int]]:
        """Create a graph of the road network with time taken to travel between points."""

        point_graph = {}

        point_graph = road_network.network

        time_graph = {}

        for point, neighbours in point_graph.items():

            key = point.location_id
            value = neighbours

            time_graph[key] = {}

            for neighbour in value:
                hours_taken = (
                    await self.time_estimator.estimate_hours_taken_between_points(
                        point, neighbour, time_of_day
                    )
                )

                time_graph[key][neighbour.location_id] = hours_taken

        return time_graph

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
