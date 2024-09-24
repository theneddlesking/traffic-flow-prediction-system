# gets the paths


from db.site import get_locations
from routing.path_costs import get_hours_taken_between_points


def get_streets_from_location_name(location_name: str) -> list[str]:
    words = location_name.split(" ")

    return [word for word in words if "_" in word]


def get_neighbours_of_location(location: dict, all_locations: list[dict]) -> list[int]:
    # get name of location

    name = location["name"]

    neighbouring_streets = get_streets_from_location_name(name)

    neighbours = []

    other_locations = all_locations.copy()

    other_locations.remove(location)

    for other_location in other_locations:
        streets = get_streets_from_location_name(other_location["name"])

        if any(street in streets for street in neighbouring_streets):
            neighbours.append(other_location["location_id"])

    return neighbours


async def create_graph(
    speed_limit: int,
    time_of_day: int,
    alpha: int,
) -> dict[int, dict[int, int]]:
    graph = {}

    all_locations = await get_locations()

    for location in all_locations:
        neighbours = get_neighbours_of_location(location, all_locations)

        location_id = location["location_id"]

        key = location_id

        graph[key] = {}

        for neighbour in neighbours:
            hours_taken = await get_hours_taken_between_points(
                location_id, neighbour, speed_limit, alpha, time_of_day
            )

            # add to cache

            graph[key][neighbour] = hours_taken

    return graph
