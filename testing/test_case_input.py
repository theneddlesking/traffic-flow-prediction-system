from routing.a_star_router import AStarRouter
from routing.basic_mfd import BasicMFD
from routing.mfd_time_estimator import MFDTimeEstimator
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
from routing.router import Router
from routing.time_graph import TimeGraph
from testing.solution import TestCaseSolution, TravelTimeTestCaseSolution

from cache import default_cache

from models import model_manager


class TestCaseInput:
    """The input data for a test case."""

    async def find_solution(self) -> TestCaseSolution:
        """Find the solution from its input."""
        raise NotImplementedError("Subclasses must implement this method.")


class TravelTimeTestCaseInput(TestCaseInput):
    """The input data need to predict the travel time."""

    def __init__(
        self,
        start_location_id: int,
        end_location_id: int,
        time_of_day: str,
        model_name: str,
        network: RoadNetwork,
        router: AStarRouter,
        time_graph: TimeGraph,
    ):
        self.start_location_id = start_location_id
        self.end_location_id = end_location_id
        self.time_of_day = time_of_day
        self.model_name = model_name

        self.network = network
        self.router = router

        self.start = self.network.points_dict[self.start_location_id]
        self.goal = self.network.points_dict[self.end_location_id]

        self.model = model_manager.get_model(self.model_name)

        self.time_graph = time_graph

    async def initialise(self):
        """Initialise the input data."""
        self.time_graph = await self.router.get_time_graph_for_model(
            self.network, self.time_of_day, self.model
        )

        return self

    async def find_solution(self) -> TravelTimeTestCaseSolution:
        """Find the solution from its input."""

        if self.model is None:
            raise ValueError("Model not found.")

        route = self.router.find_route_from_time_graph(
            self.start,
            self.goal,
            self.time_graph,
            self.network,
            self.model,
        )

        if route is None:
            return TravelTimeTestCaseSolution(None)

        return TravelTimeTestCaseSolution(route.hours_taken)
