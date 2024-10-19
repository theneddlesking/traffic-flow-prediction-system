from routing.mfd import MFD


class BasicMFD(MFD):
    """Basic implementation of a Macroscopic Fundamental Diagram (MFD)."""

    @staticmethod
    def compute_proportion(
        flow: int, capacity: int, free_flow_speed: int, alpha: int
    ) -> int:
        return 1 - alpha * (flow / capacity)
