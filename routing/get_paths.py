# gets the paths


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

    point_graph = network.network_by_id

    print("Street lookup created")

    for key, value in point_graph.items():
        print(key, value)

    # for location in all_locations:
    #     neighbours_on_same_street = street_lookup[
    #         get_street_name_from_location_name(location["name"])
    #     ]

    #     location_id = location["location_id"]

    #     key = location_id

    #     graph[key] = {}

    #     for neighbour in neighbours_on_same_street:
    #         hours_taken = await get_hours_taken_between_points(
    #             location_id, neighbour, speed_limit, alpha, time_of_day
    #         )

    #         # add to cache

    #         graph[key][neighbour] = hours_taken

    print("Graph created")

    return point_graph
