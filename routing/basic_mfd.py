from routing.mfd import MFD


class BasicMFD(MFD):
    """Basic implementation of a Macroscopic Fundamental Diagram (MFD).

    Alpha and beta are parameters that can be tuned to fit the MFD to the data.
    Alpha determines the slope of the MFD, and beta determines the minimum proportion of the MFD.
    """

    def __init__(self, alpha: int, beta: int):
        self.alpha = alpha
        self.beta = beta

    def compute_proportion(self, flow: int, capacity: int, free_flow_speed: int) -> int:
        # NOTE: alpha is very sensitive, the difference between 1 and 1.1 can be huge
        alpha = self.alpha

        # NOTE: This is a very basic implementation of the MFD, that loses a lot of nuance
        prop = 1 - alpha * (flow / capacity)
        # clamp the proportion to be between 0 and 1

        # a value of 0.0001 is used to prevent division by zero
        epilson = 0.0001

        lower_bound = epilson
        upper_bound = 1 - epilson - self.beta

        prop = max(lower_bound, min(upper_bound, prop))

        return prop
