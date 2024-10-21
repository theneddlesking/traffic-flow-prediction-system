from model.nn_model import Model
from routing.road_network import RoadNetwork
from routing.time_estimator import TimeEstimator


class TimeGraph:
    """A representation of a graph with time taken to travel between points"""

    def __init__(
        self, road_network: RoadNetwork, time_estimator: TimeEstimator, time_of_day: str
    ):
        self.road_network = road_network
        self.time_estimator = time_estimator
        self.time_of_day = time_of_day

        self.point_graph = None

    async def initialise(self, model: Model) -> "TimeGraph":
        """Async initialisation of the TimeGraph"""

        self.point_graph = await self.create_point_graph(
            self.time_of_day, self.road_network, model
        )

        return self

    async def create_point_graph(
        self,
        time_of_day: int,
        road_network: RoadNetwork,
        model: Model,
    ) -> dict[int, dict[int, int]]:
        """Create a graph of the road network with time taken to travel between points."""

        point_graph = {}

        point_graph = road_network.network

        time_graph = {}

        for point, neighbours in point_graph.items():

            key = point.location_id

            time_graph[key] = {}

            for neighbour in neighbours:
                hours_taken = (
                    await self.time_estimator.estimate_hours_taken_between_points(
                        point, neighbour, time_of_day, model
                    )
                )

                time_graph[key][neighbour.location_id] = hours_taken

        return time_graph
