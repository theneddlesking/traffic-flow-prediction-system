# site route

from fastapi import APIRouter

from routing.a_star_router import AStarRouter
from routing.basic_mfd import BasicMFD
from routing.mfd_time_estimator import MFDTimeEstimator
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork

from db.instance import site_controller

router = APIRouter()


# find optimal route between point a and point b
@router.get("/route")
async def get_route(start_location_id: int, end_location_id: int, time_of_day: str):
    """Get route"""
    # TODO add some caching logic

    # NOTE: alpha and beta are parameters that can be tuned to fit the MFD to the data
    # TODO maybe we could add a way to tune these parameters
    astar_router = AStarRouter(MFDTimeEstimator(BasicMFD(alpha=1, beta=0.3)))

    locations = site_controller.get_locations()

    routing_points = [RoutingPoint.from_location(location) for location in locations]

    network = RoadNetwork(routing_points)

    start = network.points_dict[start_location_id]
    goal = network.points_dict[end_location_id]

    routes = await astar_router.find_best_routes(start, goal, time_of_day, network)

    if len(routes) == 0:
        return {
            "error": "No path found. Could be because the start or end location is invalid."
        }

    routes_json = [route.as_json() for route in routes]

    return {"routes": routes_json}
