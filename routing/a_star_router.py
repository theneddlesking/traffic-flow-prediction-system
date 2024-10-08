from routing.astar import a_star
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
from routing.router import Router


class AStarRouter(Router):
    """A router that uses the A* algorithm to find the shortest path between two RoutingPoints."""

    def find_route(
        self, start: RoutingPoint, end: RoutingPoint, network: RoadNetwork
    ) -> list[RoutingPoint]:
        """Find the shortest route between two RoutingPoints using the A* algorithm."""

        def heuristic(a, b):
            return 0

        path = a_star(network.network, start, end, heuristic)

        for node in path:
            print(node.location_id)
