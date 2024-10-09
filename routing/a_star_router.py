from routing.astar import a_star
from routing.heuristics import Heuristics
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
from routing.router import Router


class AStarRouter(Router):
    """A router that uses the A* algorithm to find the shortest path between two RoutingPoints."""

    async def find_route(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_of_day: str,
        network: RoadNetwork,
    ) -> tuple[list[RoutingPoint], int]:
        """Find the shortest route between two RoutingPoints using the A* algorithm."""

        time_graph = await self.create_graph(time_of_day, network)

        path = a_star(
            time_graph, start.location_id, end.location_id, Heuristics.no_heuristic
        )

        if path is None:
            return None, 0

        path_points: list[RoutingPoint] = [
            network.points_dict[node.location_id] for node in path
        ]

        time_taken = sum([node.g for node in path])

        return path_points, time_taken
