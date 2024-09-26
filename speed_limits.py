import geojson

GEO_JSON = "./data/vic/Speed_Zones_August_2024.geojson"


# LIMIT = 10000

# # open as normal file

# with open(GEO_JSON) as f:

#     # save new file as only the first 10000 characters

#     with open("speed_limits_100.geojson", "w") as f2:

#         f2.write(f.read(LIMIT))

# load new file

# NEW_GEO = "./speed_limits_100.geojson"


with open(GEO_JSON) as f:

    data = geojson.load(f)

    # pretty print

    # print(geojson.dumps(data, indent=4))

    features = data["features"]

    # pretty print

    geometries = [feature["geometry"] for feature in features]

    # pretty print

    coordinates = [geometry["coordinates"] for geometry in geometries]

    # pretty print

    # print(geojson.dumps(coordinates, indent=4))

    properties = [feature["properties"] for feature in features]

    # pretty print

    speed_limits = [property["speed_limit"] for property in properties]

    # pretty print

    # print(geojson.dumps(speed_limits, indent=4))

    # map coords and speed limits with zip

    tuples = zip(coordinates, speed_limits)

    # as list of dicts

    data = [
        {"coordinates": '"' + str(coord) + '"', "speed_limit": int(speed)}
        for coord, speed in tuples
    ]

    # pretty print

    # print(geojson.dumps(data, indent=4))

    # saves a csv

    with open("./data/vic/speed_limits.csv", "w") as f2:

        f2.write("coordinates,speed_limit\n")

        for d in data:

            f2.write(f"{d['coordinates']},{d['speed_limit']}\n")
