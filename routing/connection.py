from routing.direction import Direction
from routing.haversine import haversine
from routing.intersection import Intersection
from routing.point import RoutingPoint


class IntersectionConnection:
    """An IntersectionConnection maps the RoutingPoints of an Intersection to the RoutingPoints of another Intersection."""

    def __init__(
        self,
        intersection: Intersection,
        other_intersection: Intersection,
        along_street: str,
        speed_limit: int = 60,
    ):
        self.intersection = intersection
        self.other_intersection = other_intersection
        self.along_street = along_street
        self.speed_limit = speed_limit

        # what direction is the connection
        self.direction = self.get_connection_direction()

        if self.intersection.shares_points(self.other_intersection):
            points1 = [point.location_id for point in self.intersection.points]
            points2 = [point.location_id for point in self.other_intersection.points]

            # raise a warning not an error because this is not a critical issue
            # but it is a potential issue
            print(
                f"Warning: The intersections {points1} and {points2} share points. This is not ideal."
            )

        # NOTE: It is extremely likely that there will be more than one point that connects the two intersections
        self.point_map = self.map_points()

    def get_connection_direction(self) -> Direction:
        """Get the direction of the connection between the two intersections."""

        vertical_dist = haversine(
            self.intersection.get_position()[0],
            self.intersection.get_position()[1],
            self.other_intersection.get_position()[0],
            self.intersection.get_position()[1],
        )

        horizontal_dist = haversine(
            self.intersection.get_position()[0],
            self.intersection.get_position()[1],
            self.intersection.get_position()[0],
            self.other_intersection.get_position()[1],
        )

        # check orientation of the connection

        if vertical_dist > horizontal_dist:
            return (
                Direction("N")
                if self.intersection.get_position()[0]
                < self.other_intersection.get_position()[0]
                else Direction("S")
            )

        return (
            Direction("E")
            if self.intersection.get_position()[1]
            < self.other_intersection.get_position()[1]
            else Direction("W")
        )

    def map_points(self) -> dict[RoutingPoint, RoutingPoint]:
        """Map the points of the intersection to the points of the other intersection along the street connecting them."""
        point_map = {}

        # filter points to only include points along the street connecting the two intersections
        points1 = [
            point
            for point in self.intersection.points
            if point.street_name == self.along_street
        ]

        points2 = [
            point
            for point in self.other_intersection.points
            if point.street_name == self.along_street
        ]

        # there are a few cases to consider
        # 1. When the directions are the same
        # 2. When the directions are opposite
        # 3. When the directions are perpendicular (eg. W and E), or another angle (eg. N and NW)

        # but there could be multiple matching points, but we want to find only the closest point
        # we only want the closest because we just want to enter the intersection efficiently
        # and then from there it can turn inside the intersection as needed

        # we assume that the closest point is the one that is in the opposite direction of the other intersection
        # because if you travel North up a road, you expect to be at the South end of the road
        # this is not always the case, but it is a reasonable assumption

        road_direction = self.direction

        print(
            f"Road direction: {road_direction} from {self.intersection} to {self.other_intersection}"
        )

        direction = road_direction

        for point in points1:
            opposite_direction = direction.get_opposite_direction()

            best_point = None

            for other_point in points2:
                other_direction = other_point.direction

                # best case is when the directions are opposite
                if other_direction == opposite_direction:
                    best_point = other_point

                    # we don't need to look further, this is the best case
                    break

                # second best case is when the directions are the same
                if other_direction == direction:

                    # this is better than another random point
                    best_point = other_point

            # otherwise just default it to any other point
            if len(points2) > 0 and not best_point:
                best_point = points2[0]

            if best_point:
                # save mapping
                point_map[point] = best_point
                # also save the reverse mapping
                point_map[best_point] = point

        return point_map

    def __str__(self):
        return f"IntersectionConnection({self.intersection}, {self.other_intersection}, {self.along_street} {self.direction})"

    def __repr__(self):
        return str(self)
