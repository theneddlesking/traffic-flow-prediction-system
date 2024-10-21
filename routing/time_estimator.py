from model.nn_model import Model
from routing.point import RoutingPoint


class TimeEstimator:
    """Computes the time taken to travel between two locations."""

    async def estimate_hours_taken_between_points(
        self, start: RoutingPoint, end: RoutingPoint, time_of_day: str, model: Model
    ) -> int:
        """Estimate the time taken to travel between two locations."""
        raise NotImplementedError(
            "estimate_time method must be implemented by subclass."
        )
