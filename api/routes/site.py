# site route

from fastapi import APIRouter
import numpy as np

router = APIRouter()


# from location and time of day return the flow
@router.get("/flow")
async def get_flow(site_number: int, time: str):

    # check against cache

    # do we already have the model loaded for this location

    # if not load and train the model and cache it

    # do we have a cached prediction

    # otherwise predict and cache

    # random number for now
    random_number = np.random.randint(0, 100)

    return {"flow": random_number}


# get all locations
@router.get("/locations")
async def get_locations():
    """Get all locations"""
    # get site number, name, and long lat

    # dummy data for now
    return {
        "locations": [
            {
                "site_number": 2846,
                "name": "HIGH_ST W OF WILLS_ST",
                "lat": -37.86155,
                "long": 145.05751,
            },
            {
                "site_number": 3120,
                "name": "RATHMINES_RD W of BURKE_RD",
                "lat": -37.82284,
                "long": 145.05684,
            },
            {
                "site_number": 3122,
                "name": "CANTERBURY_RD E of STANHOPE_GV",
                "lat": -37.82379,
                "long": 145.06466,
            },
        ]
    }
