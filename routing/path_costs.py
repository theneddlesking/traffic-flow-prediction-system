from math import atan2, cos, radians, sin, sqrt

from db.site import get_flow, get_location, get_max_flow


def havarsine(lat1, lon1, lat2, lon2):
    # haversine formula
    # calculate the great-circle distance between two points on the earth's surface
    # given their longitudes and latitudes
    # more info at: https://en.wikipedia.org/wiki/Haversine_formula

    R = 6371.0  # radius of the earth in km

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
    distance = R * c

    return distance


def average_flow(start_flow: int, end_flow: int):
    # there are a few ways to compute the flow between two points

    # for now we can just use a simple average

    return (start_flow + end_flow) / 2


async def get_hours_taken_between_points(
    start_location_id: int,
    end_location_id: int,
    speed_limit: int,
    alpha: float,
    time_of_day: str,
):
    # this will use the model later but for now we can just compute it as follows using a simple appracoh

    # based on some basic traffic model principles

    # time = (distance / speed) * (1 + alpha * (flow / capacity))

    # the general idea is that:
    # time = distance / speed
    # but we also need to account for traffic
    # so we can increase the time taken based on the flow of traffic

    # capacity is the maximum number of vehicles that can pass through a road without congestion eg. the car will be moving at the speed limit
    # but this is proportional to alpha

    # where flow is the flow of traffic, capacity is the capacity of the road, alpha is a constant, and speed is the speed limit

    # alpha is a constant that we can tune to make the model more accurate

    # get the distance between the two points

    # for now we can just use a simple euclidean distance

    # we can use the haversine formula to get the distance between two points on the earth's surface

    start_location = await get_location(start_location_id)
    end_location = await get_location(end_location_id)

    start_flow = await get_flow(start_location_id, time_of_day)
    end_flow = await get_flow(end_location_id, time_of_day)

    flow = average_flow(start_flow, end_flow)

    start_capacity = await get_max_flow(start_location_id)
    end_capacity = await get_max_flow(end_location_id)

    print("Getting Flow")
    print(start_flow)
    print(end_flow)
    print(flow)

    capacity = (start_capacity + end_capacity) / 2

    print("Getting Capacity")
    print(capacity)

    # haversine formula
    distance = havarsine(
        start_location["lat"],
        start_location["long"],
        end_location["lat"],
        end_location["long"],
    )

    print("Getting Distance")
    print(distance)

    # time = (distance / speed) * (1 + alpha * (flow / capacity))
    return (distance / speed_limit) * (1 + alpha * (flow / capacity))
