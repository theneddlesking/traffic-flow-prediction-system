import heapq
from typing import Callable


class Node:
    """Node class for A* algorithm"""

    def __init__(self, location_id: int, g=0, h=0, parent=None):
        self.location_id = location_id
        self.g = g
        self.h = h
        self.f = g + h
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f


def a_star(
    graph: dict[int, dict[int, int]],
    start: int,
    goal: int,
    heuristic: Callable[[int, int], int],
) -> list[str]:
    """A* algorithm to find the shortest path between two nodes in a graph."""

    open_set = []
    closed_set = set()

    start_node = Node(start, 0, heuristic(start, goal))
    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.location_id == goal:
            path = []
            while current_node:
                path.append(current_node)
                current_node = current_node.parent

            # reverse path to get start to goal
            return path[::-1]

        closed_set.add(current_node.location_id)

        for neighbor, cost in graph[current_node.location_id].items():
            if neighbor in closed_set:
                continue

            g_cost = current_node.g + cost
            h_cost = heuristic(neighbor, goal)
            neighbor_node = Node(neighbor, g_cost, h_cost, current_node)

            # check if neighbor is in open set and update if necessary
            if neighbor in [node.location_id for node in open_set]:
                for node in open_set:

                    # update g cost as we found a better path
                    if node.location_id == neighbor and g_cost < node.g:
                        open_set.remove(node)
                        break

                heapq.heappush(open_set, neighbor_node)
            else:
                heapq.heappush(open_set, neighbor_node)

    return None
