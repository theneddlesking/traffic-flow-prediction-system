# site route

from fastapi import APIRouter

from db.site import get_locations
from routing.astar import a_star
from routing.get_paths import create_graph

router = APIRouter()


# find optimal route between point a and point b
@router.get("/route")
async def get_route(start_location_id: int, end_location_id: int, time_of_day: str):
    # TODO add some caching logic

    def heuristic(a, b):
        return 0

    SPEED_LIMIT = 60

    ALPHA = 1

    graph = await create_graph(SPEED_LIMIT, time_of_day, ALPHA)

    start = start_location_id
    goal = end_location_id

    path = a_star(graph, start, goal, heuristic)

    if path is None:
        return {
            "error": "No path found. Could be because the start or end location is invalid."
        }

    all_locations = await get_locations()

    path_ids = [node.location_id for node in path]

    path_locations = []

    for location in all_locations:
        if location["location_id"] in path_ids:
            path_locations.append(location)

    time_taken = sum([node.g for node in path])

    start = path_locations[0]
    goal = path_locations[-1]

    return {
        "waypoints": path_locations,
        "hours_taken": time_taken,
    }
