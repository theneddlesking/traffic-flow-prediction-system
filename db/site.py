# site route

import sqlite3

from build_train_run import build_train_run


async def get_flow(location_id: int, time: str):
    """Get flow"""

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
        return None

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

        return prediction[0]

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
        return prediction[0]

    return None


# get all locations
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

    return locations


# get location
async def get_location(location_id: int):
    """Get location"""
    # get site number, name, and long lat

    conn = sqlite3.connect("./db/site.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, site_number, name, lat, long FROM locations WHERE id = ?",
        (location_id,),
    )

    location = cursor.fetchone()

    conn.close()

    if location is None:
        return {"error": "location not found"}

    # convert location to dict
    location = {
        "location_id": location[0],
        "site_number": location[1],
        "name": location[2],
        "lat": location[3],
        "long": location[4],
    }

    return location


# get max flow
async def get_max_flow(location_id: int):
    """Get max flow"""
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
        return None

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
        "SELECT flow FROM predictions WHERE location_id = ?",
        (location_id,),
    )

    prediction = cursor.fetchall()

    if prediction is not None:
        # close
        conn.commit()
        conn.close()

        pred_tuple = max(prediction)

        return pred_tuple[0]

    return None
