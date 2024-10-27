from testing.solution import TestCaseSolution
from testing.test_case_input import TestCaseInput
from testing.test_result import TestEvaluation, TravelTimeTestEvaluation


class TestCase:
    """A test case for a program."""

    def __init__(
        self, name: str, expected_output: TestCaseSolution, input_data: TestCaseInput
    ):
        self.name = name
        self.expected_output = expected_output
        self.input_data = input_data

    async def run(self) -> TestEvaluation:
        """Run the test case."""
        actual_output = self.input_data.find_solution()
        return TestEvaluation(self.expected_output, actual_output)


class TravelTimeTestCase(TestCase):
    """A test case for predicting travel time."""

    async def run(self) -> TravelTimeTestEvaluation:
        """Run the test case."""
        print(f"Running test case: {self.name}")
        actual_output = await self.input_data.find_solution()
        return TravelTimeTestEvaluation(self.expected_output, actual_output)
