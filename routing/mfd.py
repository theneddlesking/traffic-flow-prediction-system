class MFD:
    """Base class for the Macroscopic Fundamental Diagram (MFD)."""

    def compute_proportion(self, flow: int, capacity: int, free_flow_speed: int) -> int:
        """Compute the proportion of the free flow time taken to travel between two points."""
        raise NotImplementedError("Compute method must be implemented by subclass.")
