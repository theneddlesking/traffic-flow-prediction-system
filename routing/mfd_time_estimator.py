from model.nn_model import Model
from routing.mfd import MFD
from routing.point import RoutingPoint
from routing.time_estimator import TimeEstimator

from cache import default_cache


class MFDTimeEstimator(TimeEstimator):
    """Estimates the time taken to travel between two locations using the MFD."""

    def __init__(self, mfd: MFD):
        self.mfd = mfd

    async def estimate_hours_taken_between_points(
        self, start: RoutingPoint, end: RoutingPoint, time_of_day: str, model: Model
    ) -> int:
        """Estimate the time taken to travel between two locations."""

        free_flow_speed = 60

        # if we have the same site number this means that we are at the same intersection
        # we assume that this takes 30 seconds
        hours_taken_at_intersection = 30 / 3600

        if start.site_number == end.site_number:
            # assume that the time taken is 30 seconds for each intersection
            return hours_taken_at_intersection

        start_flow = default_cache.flow_controller.get_flow(
            start.location_id, time_of_day, model
        )

        if start_flow is None:
            # compute flow
            start_flow = default_cache.flow_controller.compute_flow(
                start.location_id, time_of_day, model
            )

        end_flow = default_cache.flow_controller.get_flow(
            end.location_id, time_of_day, model
        )

        if end_flow is None:
            # compute flow
            end_flow = await default_cache.flow_controller.compute_flow(
                end.location_id, time_of_day, model
            )

        # there are a few ways to compute the flow between two points
        # for now we can just use a simple average
        flow = (start_flow + end_flow) / 2

        start_capacity = default_cache.flow_controller.get_max_flow(
            start.location_id, model
        )
        end_capacity = default_cache.flow_controller.get_max_flow(
            end.location_id, model
        )

        # there are a few ways to compute the capacity between two points
        # for now we can just use a simple average
        capacity = (start_capacity + end_capacity) / 2

        prop = self.mfd.compute_proportion(flow, capacity, free_flow_speed)

        speed = prop * free_flow_speed

        distance = start.distance_to(end)

        time_taken = distance / speed

        return time_taken
