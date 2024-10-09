from db.controller import Controller
from db.site_model import SiteModel
from routing.location import Location
from routing.point import RoutingPoint
from routing.road_network import RoadNetwork


class SiteController(Controller):
    """SiteController class"""

    def __init__(self, model: SiteModel):
        super().__init__(model)
        self.model: SiteModel

    def get_locations(self):
        """Get all locations."""
        return [
            Location(*location_tuple) for location_tuple in self.model.get_locations()
        ]

    def get_location(self, location_id: int):
        """Get a location."""
        location_tuple = self.model.get_location(location_id)

        if location_tuple:
            return Location(*location_tuple)

        return None

    def get_intersections(self):
        """Get all intersections."""
        locations = self.get_locations()

        routing_points = [
            RoutingPoint.from_location(location) for location in locations
        ]

        road_network = RoadNetwork(routing_points)

        return road_network.intersections
