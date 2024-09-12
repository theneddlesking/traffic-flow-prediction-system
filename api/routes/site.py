# site route

import sqlite3
from fastapi import APIRouter
import numpy as np

router = APIRouter()


# from location and time of day return the flow
@router.get("/flow")
async def get_flow(location_id: int, time: str):

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

    conn = sqlite3.connect("./db/site.db")

    cursor = conn.cursor()

    cursor.execute("SELECT site_number, name, lat, long FROM locations")

    locations = cursor.fetchall()

    conn.close()

    # convert locations to dict
    locations = [
        {
            "site_number": location[0],
            "name": location[1],
            "lat": location[2],
            "long": location[3],
        }
        for location in locations
    ]

    return {"locations": locations}
