from routing.connection import IntersectionConnection
from routing.intersection import Intersection
from routing.point import RoutingPoint


class RoadNetwork:
    """A road network is a connected graph of intersections."""

    def __init__(self, routing_points: list[RoutingPoint]):
        self.points = routing_points

        self.points_dict = {point.location_id: point for point in self.points}

        self.intersections = self.find_intersections()
        self.connections = self.find_connections(self.intersections)

        # as a mapping of points
        self.network, self.network_by_id = self.build_network(self.connections)

    def build_network(
        self, connections: list[IntersectionConnection]
    ) -> tuple[dict[RoutingPoint, set[RoutingPoint]], dict[int, set[int]]]:
        """Build the road network."""

        network = {}
        network_by_id = {}

        # add connections between intersections

        for connection in connections:
            mapping = connection.point_map

            for point1, point2 in mapping.items():
                if point1 not in network:
                    network[point1] = set()
                    network_by_id[point1.location_id] = set()

                network[point1].add(point2)
                network_by_id[point1.location_id].add(point2.location_id)

        # add connections within intersections

        for intersection in self.intersections.values():

            for point in intersection.points:
                if point not in network:
                    network[point] = set()
                    network_by_id[point.location_id] = set()

                for other_point in intersection.points:

                    # same intersection
                    if point == other_point:
                        continue

                    network[point].add(other_point)
                    network_by_id[point.location_id].add(other_point.location_id)

        return network, network_by_id

    def find_intersections(self) -> dict[str, Intersection]:
        """Find all the intersections in the road network."""
        intersections = {}

        for point in self.points:
            street_names = point.street_names

            key = str(street_names)

            intersection: None | Intersection = intersections.get(key)

            if intersection is None:
                intersections[key] = Intersection(
                    street_names=street_names, points=[point]
                )
            else:
                intersection: Intersection
                intersection.add_point(point)

        # now add points that are very close to each other to the same intersection
        # this could be because of a road changing names, or a road splitting and then rejoining

        for point in self.points:
            for intersection in intersections.values():
                if intersection.is_close_to(point):
                    intersection.add_point(point)

        return intersections

    def find_connections(
        self, intersections: dict[str, Intersection]
    ) -> set[IntersectionConnection]:
        """Find all the connections between intersections."""
        connections: set[IntersectionConnection] = set()

        for intersection in intersections.values():
            for other_intersection in intersections.values():

                # same intersection
                if intersection == other_intersection:
                    continue

                for point in intersection.points:
                    for other_point in other_intersection.points:

                        # we found another intersection at this street
                        if point.street_name == other_point.street_name:

                            connection = IntersectionConnection(
                                intersection,
                                other_intersection,
                                point.street_name,
                            )

                            connections.add(connection)

        return connections
