from testing.solution import TestCaseSolution, TravelTimeTestCaseSolution


class TestEvaluation:
    """The evaluation of a test case."""

    def __init__(
        self,
        expected_output: TestCaseSolution,
        output: TestCaseSolution,
    ):
        self.expected_output = expected_output
        self.output = output

        self.evaluate(expected_output, output)

    def summarise(self) -> str:
        """Summarise the evaluation."""
        raise NotImplementedError("Subclasses must implement this method.")

    def evaluate(
        self,
        expected_output: TestCaseSolution,
        output: TestCaseSolution,
    ) -> tuple:
        """Evaluate the test."""
        raise NotImplementedError("Subclasses must implement this method.")

    def convert_to_dict(self) -> dict:
        """Convert the evaluation to a dictionary."""
        raise NotImplementedError("Subclasses must implement this method.")


class TravelTimeTestEvaluation(TestEvaluation):
    """The evaluation of a travel time test case."""

    def __init__(
        self,
        expected_output: TravelTimeTestCaseSolution,
        output: TravelTimeTestCaseSolution,
    ):
        super().__init__(expected_output, output)

        self.accuracy, self.diff, self.found_solution = self.evaluate(
            expected_output, output
        )

    def evaluate(
        self,
        expected_output: TravelTimeTestCaseSolution,
        output: TravelTimeTestCaseSolution,
    ) -> tuple[int]:
        """Evaluate the test."""

        # skip if no solution
        if output.hours_taken is None:
            return None, None, False

        hours_taken_diff = abs(expected_output.hours_taken - output.hours_taken)

        accuracy = 1 - hours_taken_diff / expected_output.hours_taken

        return accuracy, hours_taken_diff, True

    def summarise(self) -> str:
        """Summarise the evaluation."""

        if not self.found_solution:
            return "No solution found."

        return f"Accuracy: {self.accuracy:.2f}"

    def convert_to_dict(self) -> dict:
        """Convert the evaluation to a dictionary."""
        return {
            "expected_output": self.expected_output.hours_taken,
            "output": self.output.hours_taken,
            "accuracy": self.accuracy,
            "found_solution": self.found_solution,
            "diff": self.diff,
        }
