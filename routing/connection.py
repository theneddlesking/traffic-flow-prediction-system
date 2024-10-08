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

        if self.intersection.shares_points(self.other_intersection):
            points1 = [point.location_id for point in self.intersection.points]
            points2 = [point.location_id for point in self.other_intersection.points]
            raise ValueError(
                f"Intersections {self.intersection} and {self.other_intersection} share points. They should be independent. {points1} {points2}"
            )

        # NOTE: It is extremely likely that there will be more than one point that connects the two intersections
        self.point_map = self.map_points()

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

        for point in points1:
            direction = point.direction
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
