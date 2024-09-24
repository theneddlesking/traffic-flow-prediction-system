# examples

from db.site import get_location
from routing.path_costs import get_hours_taken_between_points

import asyncio

start_id = 1
end_id = 100

time_of_day = "18:00"

speed_limit = 60

# alpha is a constant that we can tune to make the model more accurate
# it represents how much the flow of traffic affects the time taken
alpha = 2

# get time taken


async def main():
    print("hello")

    hours_taken = await get_hours_taken_between_points(
        start_id, end_id, speed_limit, alpha, time_of_day
    )

    # rounded to nearest minute
    minutes_taken = round(hours_taken * 60)

    start_location = await get_location(start_id)
    end_location = await get_location(end_id)

    start_name = start_location["name"]
    end_name = end_location["name"]

    time_str = f"{minutes_taken} minutes from {start_name} to {end_name}"

    print(time_str)


asyncio.run(main())
