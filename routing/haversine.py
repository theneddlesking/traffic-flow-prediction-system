from math import atan2, cos, degrees, radians, sin, sqrt

RADIUS_OF_EARTH_KM = 6371


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points on the earth's surface given their longitudes and latitudes."""
    # haversine formula
    # calculate the great-circle distance between two points on the earth's surface
    # given their longitudes and latitudes
    # more info at: https://en.wikipedia.org/wiki/Haversine_formula

    # convert lat and long from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # change in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # haversine formula
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # distance
    distance = RADIUS_OF_EARTH_KM * c

    return distance


def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate the bearing between two points on the Earth."""

    # convert lat and long from degrees to radians
    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    # difference in longitudes
    d_lon = lon2 - lon1

    # calculate x and y components of the bearing
    x = sin(d_lon) * cos(lat2)
    y = cos(lat1) * sin(lat2) - sin(lat1) * cos(lat2) * cos(d_lon)
    bearing = atan2(x, y)

    # back to degrees
    bearing = degrees(bearing)

    # normalise
    bearing = (bearing + 360) % 360

    return bearing
