# gets the paths


from pprint import pprint
from db.site import get_locations
from routing.path_costs import get_hours_taken_between_points
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork


async def create_graph(
    speed_limit: int,
    time_of_day: int,
    alpha: int,
) -> dict[int, dict[int, int]]:
    point_graph = {}

    print("Getting all locations")

    all_locations = await get_locations()

    print("Creating Graph")

    routing_points = [
        RoutingPoint.from_raw_location_data(location) for location in all_locations
    ]

    network = RoadNetwork(routing_points)

    print("Network created")
    pprint(network.network)

    point_graph = network.network_by_id

    print("Street lookup created")

    time_graph = {}

    for key, value in point_graph.items():

        time_graph[key] = {}

        for neighbour in value:
            hours_taken = await get_hours_taken_between_points(
                key, neighbour, speed_limit, alpha, time_of_day
            )

            time_graph[key][neighbour] = hours_taken

    return time_graph
