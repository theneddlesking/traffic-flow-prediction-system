from model.nn_model import Model
from routing.astar import a_star
from routing.heuristics import Heuristics
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
from routing.route import Route
from routing.router import Router
from routing.time_estimator import TimeEstimator
from routing.time_graph import TimeGraph


class AStarRouter(Router):
    """A router that uses the A* algorithm to find the shortest path between two RoutingPoints."""

    def __init__(self, time_estimator: TimeEstimator):
        self.time_estimator = time_estimator

    async def find_route(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_of_day: str,
        network: RoadNetwork,
        model: Model,
    ) -> Route:
        """Find the shortest route between two RoutingPoints using the A* algorithm."""

        time_graph = await self.get_time_graph_for_model(network, time_of_day, model)

        return self.find_route_from_time_graph(start, end, time_graph, network, model)

    async def get_time_graph_for_model(
        self, network: RoadNetwork, time_of_day: str, model: Model
    ) -> TimeGraph:
        """Get the time graph for a model."""

        time_graph = await TimeGraph(
            network, self.time_estimator, time_of_day
        ).initialise(model)

        return time_graph

    def find_route_from_time_graph(
        self,
        start: RoutingPoint,
        end: RoutingPoint,
        time_graph: TimeGraph,
        network: RoadNetwork,
        model: Model,
    ) -> Route:
        """Find the shortest route between two RoutingPoints using the A* algorithm."""

        path = a_star(
            time_graph.point_graph,
            start.location_id,
            end.location_id,
            Heuristics.no_heuristic,
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
        model: Model,
    ) -> list[Route]:
        """Find the best routes between two points using Penalty A* algorithm."""

        time_graph = await self.get_time_graph_for_model(network, time_of_day, model)

        best_routes: list[Route] = []

        initial_route = self.find_route_from_time_graph(
            start, end, time_graph, network, model
        )

        if initial_route is None:
            return []

        best_routes.append(initial_route)

        def break_condition(
            found_routes: list[Route],
            route: Route,
            number_of_routes: int,
            search_attempts: int,
        ) -> bool:
            """Check when to stop the search for best routes."""
            # NOTE: you could have a smarter break condition
            return number_of_routes >= 5 or search_attempts >= 10

        search_attempts = 0

        # NOTE: this is an arbitrary penalty, could we tweak this or make it dynamic?
        penalty_hours = 1 / 60

        while not break_condition(
            best_routes, best_routes[-1], len(best_routes), search_attempts
        ):
            search_attempts += 1

            # penalise the previous route
            time_graph = self.penalise_route(best_routes[-1], penalty_hours, time_graph)

            # find the next best route
            next_best_route = self.find_route_from_time_graph(
                start, end, time_graph, network, model
            )

            # TODO check route instead of exact match, check if they are substantially different
            # check this by comparing the SCAT site numbers, eg. don't just run around the intersection

            # already found the same route or no more routes to find
            print("checking next best route")
            print(next_best_route)
            if next_best_route is None or next_best_route in best_routes:
                break

            best_routes.append(next_best_route)

        # get the actual time taken, not the penalised time

        # TODO this could be simplified somehow, but it should be pretty fast
        # because there won't be many points in the phony network

        actual_routes: list[Route] = []

        for route in best_routes:

            # phony network that only contains the waypoints of the route
            phony_network = RoadNetwork(route.waypoints)

            new_time_graph = await self.get_time_graph_for_model(
                phony_network, time_of_day, model
            )

            # find the actual time taken
            actual_route = self.find_route_from_time_graph(
                start, end, new_time_graph, phony_network, model
            )

            actual_routes.append(actual_route)

        # technically the phony routes could yield the same route even if they were different on the original network
        def remove_duplicate_routes(routes: list[Route]) -> list[Route]:
            """Remove duplicate routes."""
            unique_routes = []

            for route in routes:
                if route not in unique_routes:
                    unique_routes.append(route)

            return unique_routes

        # remove duplicates
        # NOTE: hacky and slow, could be improved
        no_duplicates = remove_duplicate_routes(actual_routes)

        # sort them so that the fastest route is first
        no_duplicates.sort(key=lambda route: route.hours_taken)

        return no_duplicates

    def penalise_route(
        self, route: Route, penalty_hours: int, time_graph: TimeGraph
    ) -> TimeGraph:
        """Penalise a route on the graph by adding a penalty to the edges."""

        # edges to penalise
        for waypoint in route.waypoints:
            # get the neighbours of the waypoint
            neighbours = time_graph.point_graph[waypoint.location_id]

            for neighbour_id, _ in neighbours.items():

                # penalise the edge
                time_graph.point_graph[waypoint.location_id][
                    neighbour_id
                ] += penalty_hours

        return time_graph
