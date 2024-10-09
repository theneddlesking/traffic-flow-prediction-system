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

    astar_router = AStarRouter(MFDTimeEstimator(BasicMFD))

    locations = site_controller.get_locations()

    routing_points = [RoutingPoint.from_location(location) for location in locations]

    network = RoadNetwork(routing_points)

    start = network.points_dict[start_location_id]
    goal = network.points_dict[end_location_id]

    path, time_taken = await astar_router.find_route(start, goal, time_of_day, network)

    if path is None:
        return {
            "error": "No path found. Could be because the start or end location is invalid."
        }

    return {
        "waypoints": path,
        "hours_taken": time_taken,
    }
