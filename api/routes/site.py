# site route

import sqlite3
from fastapi import APIRouter
import numpy as np

from build_train_run import build_train_run

router = APIRouter()


# from location and time of day return the flow
@router.get("/flow")
async def get_flow(location_id: int, time: str):

    # get location data from db
    conn = sqlite3.connect("./db/site.db")

    cursor = conn.cursor()

    # sql injection??
    cursor.execute(
        "SELECT id, site_number, name, lat, long FROM locations WHERE id = ?",
        (location_id,),
    )

    location = cursor.fetchone()

    if location is None:
        return {"error": "location not found"}

    # convert to dict
    location = {
        "location_id": location[0],
        "site_number": location[1],
        "name": location[2],
        "lat": location[3],
        "long": location[4],
    }

    # check if we have already made predictions for this location

    cursor.execute(
        "SELECT flow FROM predictions WHERE location_id = ? AND time = ?",
        (location_id, time),
    )

    prediction = cursor.fetchone()

    if prediction is not None:
        # close
        conn.commit()
        conn.close()

        return {"flow": prediction[0]}

    # else we need to train and run the model
    df = build_train_run(location["name"])

    # save to db
    for index, row in df.iterrows():
        cursor.execute(
            "INSERT INTO predictions (location_id, time, flow) VALUES (?, ?, ?)",
            (location_id, row["time"], row["gru"]),
        )

    cursor.execute(
        "SELECT flow FROM predictions WHERE location_id = ? AND time = ?",
        (location_id, time),
    )

    prediction = cursor.fetchone()

    # close
    conn.commit()
    conn.close()

    if prediction is not None:
        return {"flow": prediction[0]}

    return {"error": "flow not found"}


# get all locations
@router.get("/locations")
async def get_locations():
    """Get all locations"""
    # get site number, name, and long lat

    conn = sqlite3.connect("./db/site.db")

    cursor = conn.cursor()

    cursor.execute("SELECT id, site_number, name, lat, long FROM locations")

    locations = cursor.fetchall()

    conn.close()

    # convert locations to dict
    locations = [
        {
            "location_id": location[0],
            "site_number": location[1],
            "name": location[2],
            "lat": location[3],
            "long": location[4],
        }
        for location in locations
    ]

    return {"locations": locations}
