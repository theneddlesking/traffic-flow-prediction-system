class Direction:
    """A direction of road as N, S, E, W, NE, NW, SE, SW."""

    def __init__(self, direction: str):
        self.value = direction

    def get_opposite_direction(self) -> "Direction":
        """Get the opposite direction of a given direction."""

        def get_opposite_str(direction: str) -> str:
            if direction == "N":
                return "S"
            if direction == "S":
                return "N"
            if direction == "E":
                return "W"
            if direction == "W":
                return "E"
            if direction == "NE":
                return "SW"
            if direction == "NW":
                return "SE"
            if direction == "SE":
                return "NW"
            if direction == "SW":
                return "NE"
            raise ValueError(f"Invalid direction: {direction}")

        return Direction(get_opposite_str(self.value))

    def __eq__(self, other: "Direction"):
        return self.value == other.value

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value
