# gets the paths


def get_neighbours(location_id: int):
    # lookup from db

    # hardcoding for now
    neighbours = {
        1: [2, 3, 4],
        2: [1, 3, 4],
        3: [1, 2, 4],
        4: [1, 2, 3],
    }

    return neighbours[location_id]
