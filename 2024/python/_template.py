from solution_base import AocSolution, solution, InputSource


class DayX(AocSolution):

    @property
    def title(self) -> str:
        return "Puzzle Title"  # TODO: Replace with puzzle title

    @solution()  # Add expected result when known
    def solve_part1(self, input_data: InputSource) -> int:
        """Solve part 1 of the puzzle."""
        self.logger.debug("Starting part 1 solution")

        # Your solution here
        return 0

    @solution()  # Add expected result when known
    def solve_part2(self, input_data: str) -> int:
        """Solve part 2 of the puzzle."""
        self.logger.debug("Starting part 2 solution")

        # Your solution here
        return 0


if __name__ == "__main__":
    solution = DayX()
    part = 1

    # Run with example data in debug mode
    solution.run(part=part, is_example=True, debug=True)

    # Run both parts with real input
    # solution.run()
