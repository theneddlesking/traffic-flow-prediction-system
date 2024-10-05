# site route

from fastapi import APIRouter

from db.site import get_flow, get_location, get_locations

router = APIRouter()


# from location and time of day return the flow
@router.get("/flow")
async def get_flow_route(location_id: int, time: str):
    """Get flow"""

    flow = await get_flow(location_id, time)

    if flow is not None:
        return {"flow": flow}

    return {
        "error": "Flow not found. Could be because the location or time is invalid."
    }


# get all locations
@router.get("/locations")
async def get_locations_route():
    """Get all locations"""
    return {
        "locations": await get_locations(),
    }


# get location
@router.get("/location")
async def get_location_route(location_id: int):
    """Get location"""
    return {
        "location": await get_location(location_id),
    }
