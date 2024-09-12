# site route

from fastapi import APIRouter

router = APIRouter()


# find optimal route between point a and point b
@router.get("/route")
async def get_flow(start_location_id: int, end_location_id: int):
    # check against cache

    # do we already have the model loaded for this location

    # if not load and train the model and cache it

    # do we have a cached prediction

    # otherwise predict and cache

    return {
        "start_site_number": start_location_id,
        "end_site_number": end_location_id,
        "flow": 100,
    }
