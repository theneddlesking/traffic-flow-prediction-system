from routing.point import RoutingPoint


class Intersection:
    """An Intersection is a set of RoutingPoints where two streets intersect under two given street names."""

    # Assumes that an intersection is defined by two streets, not always the case in practice
    # However, this simplification should still be sufficient because in the context of routing, an intersection is just a method of changing streets

    # So if there are 2+ intersections on top of each other, to represent the intersection of 3+ streets, this okay
    # Because the router just wants to define the turns that can be made at an intersection
    # It doesn't care that there are multiple intersections at the same point

    # For 3+ intersections at the same point, the router may take an extra turn to get to the desired street
    # This is almost an impossible problem to solve without the actual street data

    def __init__(self, street_names: set[str], points: list[RoutingPoint]):
        self.street_names = street_names
        self.points = points

    def add_point(self, point: RoutingPoint):
        """Add a point to the intersection."""
        self.points.append(point)

    def shares_points(self, other_intersection: "Intersection") -> bool:
        """Check if two intersections share points."""
        return any(point in other_intersection.points for point in self.points)

    def __str__(self):
        return f"Intersection({self.street_names})"

    def __hash__(self):
        return hash(str(self))
