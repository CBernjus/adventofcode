import itertools

from solution_base import AocSolution, solution, InputSource

# -------------------
# PART 1: Description
# -------------------

# You find yourselves on the roof of a top-secret Easter Bunny installation.

# While The Historians do their thing, you take a look at the familiar huge
# antenna. Much to your surprise, it seems to have been reconfigured to emit
# a signal that makes people 0.1% more likely to buy Easter Bunny brand
# Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

# Scanning across the city, you find that there are actually many such
# antennas. Each antenna is tuned to a specific frequency indicated by a
# single lowercase letter, uppercase letter, or digit. You create a map (your
# puzzle input) of these antennas. For example:

# ............
# ........0...
# .....0......
# .......0....
# ....0.......
# ......A.....
# ............
# ............
# ........A...
# .........A..
# ............
# ............

# The signal only applies its nefarious effect at specific antinodes based on
# the resonant frequencies of the antennas. In particular, an antinode occurs
# at any point that is perfectly in line with two antennas of the same
# frequency - but only when one of the antennas is twice as far away as the
# other. This means that for any pair of antennas with the same frequency,
# there are two antinodes, one on either side of them.

# So, for these two antennas with frequency a, they create the two antinodes
# marked with #:

# ..........
# ...#......
# ..........
# ....a.....
# ..........
# .....a....
# ..........
# ......#...
# ..........
# ..........

# Adding a third antenna with the same frequency creates several more
# antinodes. It would ideally add four antinodes, but two are off the right
# side of the map, so instead it adds only two:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......#...
# ..........
# ..........

# Antennas with different frequencies don't create antinodes; A and a count
# as different frequencies. However, antinodes can occur at locations that
# contain antennas. In this diagram, the lone antenna with frequency capital
# A creates no antinodes but has a lowercase-a-frequency antinode at its location:

# ..........
# ...#......
# #.........
# ....a.....
# ........a.
# .....a....
# ..#.......
# ......A...
# ..........
# ..........

# The first example has antennas with two different frequencies, so the
# antinodes they create look like this, plus an antinode overlapping the
# topmost A-frequency antenna:

# ......#....#
# ...#....0...
# ....#0....#.
# ..#....0....
# ....0....#..
# .#....A.....
# ...#........
# #......#....
# ........A...
# .........A..
# ..........#.
# ..........#.

# Because the topmost A-frequency antenna overlaps with a 0-frequency
# antinode, there are 14 total unique locations that contain an antinode
# within the bounds of the map.

# Calculate the impact of the signal. How many unique locations within
# the bounds of the map contain an antinode?

# -------------------
# PART 2: Description
# -------------------

# Watching over your shoulder as you work, one of The Historians asks if you
# took the effects of resonant harmonics into your calculations.

# Whoops!

# After updating your model, it turns out that an antinode occurs at any grid
# position exactly in line with at least two antennas of the same frequency,
# regardless of distance. This means that some of the new antinodes will
# occur at the position of each antenna (unless that antenna is the only one
# of its frequency).

# So, these three T-frequency antennas now create many antinodes:

# T....#....
# ...T......
# .T....#...
# .........#
# ..#.......
# ..........
# ...#......
# ..........
# ....#.....
# ..........

# In fact, the three T-frequency antennas are all exactly in line with two
# antennas, so they are all also antinodes! This brings the total number of
# antinodes in the above example to 9.

# The original example now has 34 antinodes, including the antinodes that
# appear on every antenna:

# ##....#....#
# .#.#....0...
# ..#.#0....#.
# ..##...0....
# ....0....#..
# .#...#A....#
# ...#..#.....
# #....#.#....
# ..#.....A...
# ....#....A..
# .#........#.
# ...#......##

# Calculate the impact of the signal using this updated model. How many
# unique locations within the bounds of the map contain an antinode?


Coord = tuple[int, int]
Grid = list[list[str]]


def find_antennas(grid: Grid) -> dict[str, list[Coord]]:
    antennas = {}
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell.isalnum():
                antennas.setdefault(cell, []).append((x, y))
    return antennas


def find_direct_antinodes(antennas_by_type: dict[str, list[Coord]]) -> dict[str, set[Coord]]:
    antinodes = dict()
    for t, antennas in antennas_by_type.items():
        antinodes.setdefault(t, set())
        permutations = list(itertools.permutations(antennas, 2))
        for a, b in permutations:
            xa, ya = a
            xb, yb = b
            dx = xb - xa
            dy = yb - ya
            antinodes.get(t).add((xa + 2 * dx, ya + 2 * dy))
    return antinodes


def find_all_antinodes(antennas_by_type: dict[str, list[Coord]], grid: Grid) -> dict[str, set[Coord]]:
    antinodes = dict()
    for t, antennas in antennas_by_type.items():
        antinodes.setdefault(t, set())
        permutations = list(itertools.permutations(antennas, 2))
        for a, b in permutations:
            xa, ya = a
            xb, yb = b
            dx = xb - xa
            dy = yb - ya
            i = 1
            while True:
                new_x, new_y = xa + i * dx, ya + i * dy
                if not is_in_bounds(grid, (new_x, new_y)):
                    break
                antinodes.get(t).add((new_x, new_y))
                i += 1
    return antinodes


def is_in_bounds(grid: Grid, coord: Coord) -> bool:
    x, y = coord
    return 0 <= x < len(grid[0]) and 0 <= y < len(grid)


class Day8(AocSolution):

    @property
    def title(self) -> str:
        return "Resonant Collinearity"

    @property
    def question_part1(self) -> str:
        return "How many unique locations within the bounds of the map contain an antinode?"

    @property
    def question_part2(self) -> str:
        return "How many unique locations within the bounds of the map contain an antinode using the new model?"

    @solution(344)
    def solve_part1(self, input_data: InputSource) -> int:
        grid = input_data.read_char_grid()
        antennas_by_type = find_antennas(grid)
        antinodes = find_direct_antinodes(antennas_by_type)
        all_antinodes = set(itertools.chain(*antinodes.values()))
        antinodes_in_bounds = list(filter(lambda coord: is_in_bounds(grid, coord), all_antinodes))
        return len(antinodes_in_bounds)

    @solution(1182)
    def solve_part2(self, input_data: InputSource) -> int:
        grid = input_data.read_char_grid()
        antennas_by_type = find_antennas(grid)
        antinodes = find_all_antinodes(antennas_by_type, grid)
        all_antinodes = set(itertools.chain(*antinodes.values()))
        antinodes_in_bounds = list(filter(lambda coord: is_in_bounds(grid, coord), all_antinodes))
        return len(antinodes_in_bounds)


if __name__ == "__main__":
    solution = Day8()

    # Run with example data in debug mode
    # solution.run(part=1, is_example=True, debug=True)

    # Run both parts with real input
    solution.run()
