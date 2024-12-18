from solution_base import AocSolution, solution, InputSource

# -------------------
# PART 1: Description
# -------------------

# The ancient civilization on Pluto was known for its ability to manipulate
# spacetime, and while The Historians explore their infinite corridors,
# you've noticed a strange set of physics-defying stones.

# At first glance, they seem like normal stones: they're arranged in a
# perfectly straight line, and each stone has a number engraved on it.

# The strange part is that every time you blink, the stones change.

# Sometimes, the number engraved on a stone changes. Other times, a stone
# might split in two, causing all the other stones to shift over a bit to
# make room in their perfectly straight line.

# As you observe them for a while, you find that the stones have a consistent
# behavior. Every time you blink, the stones each simultaneously change
# according to the first applicable rule in this list:

# - If the stone is engraved with the number 0, it is replaced by a stone
#   engraved with the number 1.
# - If the stone is engraved with a number that has an even number of
#   digits, it is replaced by two stones. The left half of the digits are
#   engraved on the new left stone, and the right half of the digits are
#   engraved on the new right stone. (The new numbers don't keep extra
#   leading zeroes: 1000 would become stones 10 and 0.)
# - If none of the other rules apply, the stone is replaced by a new
#   stone; the old stone's number multiplied by 2024 is engraved on the
#   new stone.

# No matter how the stones change, their order is preserved, and they stay on
# their perfectly straight line.

# How will the stones evolve if you keep blinking at them? You take a note of
# the number engraved on each stone in the line (your puzzle input).

# If you have an arrangement of five stones engraved with the numbers
# 0 1 10 99 999 and you blink once, the stones transform as follows:

# - The first stone, 0, becomes a stone marked 1.
# - The second stone, 1, is multiplied by 2024 to become 2024.
# - The third stone, 10, is split into a stone marked 1 followed by a
#   stone marked 0.
# - The fourth stone, 99, is split into two stones marked 9.
# - The fifth stone, 999, is replaced by a stone marked 2021976.

# So, after blinking once, your five stones would become an arrangement of
# seven stones engraved with the numbers 1 2024 1 0 9 9 2021976.

# Here is a longer example:

# Initial arrangement:
# 125 17

# After 1 blink:
# 253000 1 7

# After 2 blinks:
# 253 0 2024 14168

# After 3 blinks:
# 512072 1 20 24 28676032

# After 4 blinks:
# 512 72 2024 2 0 2 4 2867 6032

# After 5 blinks:
# 1036288 7 2 20 24 4048 1 4048 8096 28 67 60 32

# After 6 blinks:
# 2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2

# In this example, after blinking six times, you would have 22 stones. After
# blinking 25 times, you would have 55312 stones!

# Consider the arrangement of stones in front of you. How many stones will
# you have after blinking 25 times?

# -------------------
# PART 2: Description
# -------------------

# The Historians sure are taking a long time. To be fair, the infinite corridors are very large.

# How many stones would you have after blinking a total of 75 times?

Stone = tuple[int, str]


def read_stones(input_data: InputSource) -> list[Stone]:
    return [(int(stone), stone) for stone in input_data.read_raw().split(' ')]


def evolve_stone(stone: Stone) -> list[Stone]:
    num, char = stone
    if num == 0:
        return [(1, '1')]
    if len(char) % 2 == 0:
        middle = len(char) // 2
        left, right_num = char[:middle], int(char[middle:])
        return [(int(left), left), (right_num, str(right_num))]
    new_num = num * 2024
    return [(new_num, str(new_num))]


def evolve_recursive(stone: Stone, cache: dict[tuple[Stone, int], int], steps: int) -> int:
    """Recursively evolve a stone up to the given number of steps and cache the result."""
    if steps == 0:
        return 1  # Base case: 1 stone remains at step 0

    if (stone, steps) in cache:
        return cache[(stone, steps)]

    total_stones = 0
    for evolved_stone in evolve_stone(stone):
        total_stones += evolve_recursive(evolved_stone, cache, steps - 1)

    cache[(stone, steps)] = total_stones
    return total_stones


def blink(stones: list[Stone]) -> list[Stone]:
    new_stones = []
    for stone in stones:
        new_stones.extend(evolve_stone(stone))
    return new_stones


class Day11(AocSolution):

    @property
    def title(self) -> str:
        return "Plutonian Pebbles"

    @property
    def question_part1(self) -> str:
        return "How many stones will you have after blinking 25 times?"

    @property
    def question_part2(self) -> str:
        return "How many stones would you have after blinking a total of 75 times?"

    @solution(217443)
    def solve_part1(self, input_data: InputSource) -> int:
        stones = read_stones(input_data)
        for _ in range(25):
            stones = blink(stones)
        return len(stones)

    @solution(257246536026785)
    def solve_part2(self, input_data: InputSource) -> int:
        stones = read_stones(input_data)
        cache = {}

        total_stones = 0
        for i, stone in enumerate(stones):
            total_stones += evolve_recursive(stone, cache, 75)

        return total_stones


if __name__ == "__main__":
    solution = Day11()

    # Run with example data in debug mode
    # solution.run(part=1, is_example=False, example_suffix='larger', debug=True)

    # Run both parts with real input
    solution.run()
