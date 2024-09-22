# site route

from fastapi import APIRouter

router = APIRouter()


# find optimal route between point a and point b
@router.get("/route")
async def get_route(start_location_id: int, end_location_id: int):
    # no need to cache cause everything should be fast and already exist

    # plan:

    # 1. get path costs from db
    # 2. if path costs don't exist, calculate path costs - this will do some caching maybe
    #   - to get path costs we need to get the paths
    #   - we can hardcode a few of the paths for now

    # 3. get the optimal path using astar, heuristic is euclidean distance but idk it will be admisible because speed limits
    # maybe we can just estimate the path cost with some custom formula, or make a model that predicts the path cost

    # 4. return the waypoints

    return {"waypoints": []}
