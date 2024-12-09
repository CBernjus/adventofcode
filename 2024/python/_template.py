from solution_base import AocSolution, solution, InputSource

# -------------------
# PART 1: Description
# -------------------

#

# -------------------
# PART 2: Description
# -------------------

#


class DayX(AocSolution):

    @property
    def title(self) -> str:
        return "PuzzleTitle"

    @property
    def question_part1(self) -> str:
        return "Question1"

    @property
    def question_part2(self) -> str:
        return "Question2"

    @solution()
    def solve_part1(self, input_data: InputSource) -> int:

        return 0

    @solution()
    def solve_part2(self, input_data: InputSource) -> int:

        return 0


if __name__ == "__main__":
    solution = DayX()

    # Run with example data in debug mode
    solution.run(part=1, is_example=True, debug=True)

    # Run both parts with real input
    # solution.run()
