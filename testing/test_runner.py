from testing.test_case import TestCase
from testing.test_result import TestEvaluation


class TestRunner:
    """A class to test a program."""

    def __init__(self):
        self.test_cases: list[TestCase] = []

    def add_test_case(self, test_case):
        """Add a test case to the tester."""
        self.test_cases.append(test_case)

    async def run(self):
        """Run all the test cases."""
        evaluations: list[TestEvaluation] = []

        for test_case in self.test_cases:
            result = await test_case.run()

            evaluations.append(result)

        return evaluations
