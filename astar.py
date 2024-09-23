# Example usage:
import asyncio
from db.site import get_location
from routing.astar import a_star
from routing.path_costs import get_hours_taken_between_points


graph = {
    "A": {"B": 1, "C": 4},
    "B": {"A": 1, "D": 2, "E": 5},
    "C": {"A": 4, "E": 1},
    "D": {"B": 2, "E": 3},
    "E": {"B": 5, "C": 1, "D": 3},
}


def convert_letter_to_id(letter):
    return ord(letter) - 64


def convert_id_to_letter(id):
    return chr(id + 64)


def heuristic(a, b):
    letter = convert_id_to_letter(b)

    return {
        "A": 5,
        "B": 4,
        "C": 2,
        "D": 2,
        "E": 0,
    }[letter]


start = convert_letter_to_id("A")
goal = convert_letter_to_id("E")

speed_limit = 60
alpha = 2
time_of_day = "18:00"


def build_graph(original_graph):
    graph = {}
    for key, value in original_graph.items():
        graph[convert_letter_to_id(key)] = {
            convert_letter_to_id(k): v for k, v in value.items()
        }
    return graph


graph = build_graph(graph)


async def replace_path_costs(graph):
    new_graph = {}
    for key, value in graph.items():
        new_graph[key] = {
            k: await get_hours_taken_between_points(
                key, k, speed_limit, alpha, time_of_day
            )
            for k in value
        }
    return new_graph


graph = asyncio.run(replace_path_costs(graph))

path = a_star(graph, start, goal, heuristic)


async def convert_id_to_name(ids):
    return [await get_location(id) for id in ids]


path = asyncio.run(convert_id_to_name(path))

path_names = [p["name"] for p in path]

print(path_names)
