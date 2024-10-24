from routing.a_star_router import AStarRouter
from routing.basic_mfd import BasicMFD
from routing.mfd_time_estimator import MFDTimeEstimator
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork
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
    ):
        self.start_location_id = start_location_id
        self.end_location_id = end_location_id
        self.time_of_day = time_of_day
        self.model_name = model_name

    async def find_solution(self) -> TravelTimeTestCaseSolution:
        """Find the solution from its input."""
        astar_router = AStarRouter(MFDTimeEstimator(BasicMFD(alpha=0.8, beta=0.3)))

        locations = default_cache.site_controller.get_locations()

        routing_points = [
            RoutingPoint.from_location(location) for location in locations
        ]

        network = RoadNetwork(routing_points)

        start = network.points_dict[self.start_location_id]
        goal = network.points_dict[self.end_location_id]

        model = model_manager.get_model(self.model_name)

        if model is None:
            raise ValueError("Model not found.")

        route = await astar_router.find_route(
            start, goal, self.time_of_day, network, model
        )

        if route is None:
            return TravelTimeTestCaseSolution(None)

        return TravelTimeTestCaseSolution(route.hours_taken)
