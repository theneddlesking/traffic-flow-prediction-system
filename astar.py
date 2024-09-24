# Example usage:
import asyncio
from db.site import get_locations
from routing.astar import a_star
from routing.get_paths import create_graph


def heuristic(a, b):
    return 0


TIME_OF_DAY = "18:00"

SPEED_LIMIT = 60

ALPHA = 1

graph = asyncio.run(create_graph(SPEED_LIMIT, TIME_OF_DAY, ALPHA))

start = 1
goal = 120

path = a_star(graph, start, goal, heuristic)

all_locations = asyncio.run(get_locations())

path_ids = [node.location_id for node in path]

path_locations = []

for location in all_locations:
    if location["location_id"] in path_ids:
        path_locations.append(location)

time_taken = sum([node.g for node in path])

path_names = [location["name"] for location in path_locations]

start = path_locations[0]
goal = path_locations[-1]

print("Start:")
print(start)

print("Goal:")
print(goal)

print("Path:")
print(path_names)

print("Time taken:")

in_minutes = time_taken * 60

minutes = in_minutes % 60

hours = in_minutes // 60

print(f"{hours} hours {minutes} minutes")
