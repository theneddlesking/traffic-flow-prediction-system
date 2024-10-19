from routing.astar import a_star
from routing.heuristics import Heuristics
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
from routing.route import Route
from routing.router import Router


class AStarRouter(Router):
    """A router that uses the A* algorithm to find the shortest path between two RoutingPoints."""

    async def find_route(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_of_day: str,
        network: RoadNetwork,
    ) -> Route:
        """Find the shortest route between two RoutingPoints using the A* algorithm."""

        time_graph = await self.create_graph(time_of_day, network)

        return self.find_route_from_time_graph(start, end, time_graph, network)

    def find_route_from_time_graph(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_graph: dict[int, dict[int, int]],
        network: RoadNetwork,
    ) -> Route:
        """Find the shortest route between two RoutingPoints using the A* algorithm."""

        path = a_star(
            time_graph, start.location_id, end.location_id, Heuristics.no_heuristic
        )

        if path is None:
            return None

        path_points: list[RoutingPoint] = [
            network.points_dict[node.location_id] for node in path
        ]

        time_taken = path[-1].g

        return Route(path_points, time_taken)

    async def find_best_routes(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_of_day: str,
        network: RoadNetwork,
    ) -> list[Route]:
        """Find the best routes between two points using Penalty A* algorithm."""

        time_graph = await self.create_graph(time_of_day, network)

        best_routes = []

        initial_route = self.find_route_from_time_graph(start, end, time_graph, network)

        if initial_route is None:
            return []

        best_routes.append(initial_route)

        # TODO implement penalty A* algorithm

        return best_routes
