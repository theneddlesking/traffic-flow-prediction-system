# gets the paths


from db.site import get_locations
from routing.path_costs import get_hours_taken_between_points


def get_streets_from_location_name(location_name: str) -> list[str]:
    words = location_name.split(" ")

    streets = [word for word in words if "_" in word]

    return [streets[0]]


def get_opposite_direction(direction: str) -> str:
    if direction == "N":
        return "S"
    elif direction == "S":
        return "N"
    elif direction == "E":
        return "W"
    elif direction == "W":
        return "E"
    elif direction == "NE":
        return "SW"
    elif direction == "NW":
        return "SE"
    elif direction == "SE":
        return "NW"
    elif direction == "SW":
        return "NE"
    else:
        return None


def get_neighbours_from_scat(location: dict, all_locations: list[dict]) -> list[int]:

    other_locations = all_locations.copy()

    other_locations.remove(location)

    neighbours = []

    for other_location in other_locations:
        if other_location["site_number"] == location["site_number"]:

            neighbours.append(other_location["location_id"])

    return neighbours


def get_direction_from_location_name(location_name: str) -> str:
    cardinal_directions = ["N", "S", "E", "W"]

    inter_cardinal_directions = ["NE", "NW", "SE", "SW"]

    all_directions = cardinal_directions + inter_cardinal_directions

    words = location_name.split(" ")

    for word in words:
        if word in all_directions:
            return word

    return None


def get_neighbours_of_location(location: dict, all_locations: list[dict]) -> list[int]:
    # get name of location

    name = location["name"]

    neighbouring_streets = get_streets_from_location_name(name)
    neighbours = []

    other_locations = all_locations.copy()

    other_locations.remove(location)

    direction = get_direction_from_location_name(name)

    # go through all other locations and check if they are on the same street
    for other_location in other_locations:

        # get streets of other location
        streets = get_streets_from_location_name(other_location["name"])

        for street in streets:

            if street not in neighbouring_streets:
                continue

            other_direction = get_direction_from_location_name(other_location["name"])

            if other_direction == get_opposite_direction(direction):
                neighbours.append(other_location["location_id"])

    # add some neighbours from same scat in case they don't have the same street name
    neighbours = set(neighbours + get_neighbours_from_scat(location, all_locations))

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
