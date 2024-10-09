# site route

from fastapi import APIRouter

from db.instance import site_controller, basic_flow_controller

router = APIRouter()


# from location and time of day return the flow
@router.get("/flow")
async def get_flow_route(location_id: int, time: str):
    """Get flow"""

    flow = basic_flow_controller.get_flow(location_id, time)

    if flow is None:
        # compute flow
        flow = await basic_flow_controller.compute_flow(location_id, time)

    if flow is not None:
        return {"flow": flow}

    return {
        "error": "Flow not found. Could be because the location or time is invalid."
    }


# get all locations
@router.get("/locations")
async def get_locations_route():
    """Get all locations"""
    locations = site_controller.get_locations()
    return {"locations": locations}


# get location
@router.get("/location")
async def get_location_route(location_id: int):
    """Get location"""
    location = site_controller.get_location(location_id)

    if location is not None:
        return {"location": location}

    return {"error": "Location not found."}
