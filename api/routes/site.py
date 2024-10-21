# site route

from fastapi import APIRouter
from cache import default_cache

from models import model_manager

router = APIRouter()


# get all models in string form
@router.get("/models")
async def get_models():
    """Get all models"""

    models = model_manager.get_models()

    model_names = [model.name for model in models]

    return {"models": model_names}


# get all locations
@router.get("/locations")
async def get_locations():
    """Get all locations"""
    locations = default_cache.site_controller.get_locations()
    return {"locations": locations}


# get location
@router.get("/location")
async def get_location(location_id: int):
    """Get location"""
    location = default_cache.site_controller.get_location(location_id)

    if location is not None:
        return {"location": location}

    return {"error": "Location not found."}


# get intersections
@router.get("/intersections")
async def get_intersections():
    """Get all intersections"""
    intersections = default_cache.site_controller.get_intersections()

    intersections_json = [intersection.as_json() for intersection in intersections]

    return {"intersections": intersections_json}


# get connections
@router.get("/connections")
async def get_connections():
    """Get all connections"""
    connections = list(default_cache.site_controller.get_connections())

    connections_json = [connection.as_json() for connection in connections]

    return {"connections": connections_json}
