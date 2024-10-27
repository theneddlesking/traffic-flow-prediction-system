# site route

from fastapi import APIRouter

from routing.a_star_router import AStarRouter
from routing.basic_mfd import BasicMFD
from routing.mfd_time_estimator import MFDTimeEstimator
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork

from models import model_manager

from cache import default_cache
from time_utils import TimeUtils

router = APIRouter()


# find optimal route between point a and point b
@router.get("/route")
async def get_route(
    start_location_id: int, end_location_id: int, time_of_day: str, model_name: str
):
    """Get route"""

    # round time to nearest 15 minutes

    time_of_day = TimeUtils.round_time_to_nearest_quarter(time_of_day)

    astar_router = AStarRouter(MFDTimeEstimator(BasicMFD(alpha=0.8, beta=0.3)))

    locations = default_cache.site_controller.get_locations()

    routing_points = [RoutingPoint.from_location(location) for location in locations]

    network = RoadNetwork(routing_points)

    start = network.points_dict[start_location_id]
    goal = network.points_dict[end_location_id]

    model = model_manager.get_model(model_name)

    if model is None:
        return {"error": "Model not found."}

    routes = await astar_router.find_best_routes(
        start, goal, time_of_day, network, model
    )

    if len(routes) == 0:
        return {
            "error": "No path found. Could be because the start or end location is invalid."
        }

    if any(route is None for route in routes):
        return {
            "error": "An invalid route was generated. This is likely because the server is not fully loaded. Please restart the \
            server and wait a few moments before making a request."
        }

    return {"routes": [route.as_json() for route in routes]}
