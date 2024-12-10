from enum import Enum
from typing import Set, TypeAlias

from solution_base import AocSolution, solution, InputSource


# logging.basicConfig(level=logging.DEBUG)

# -------------------
# PART 1: Description
# -------------------

# The Historians use their fancy device again, this time to whisk you all
# away to the North Pole prototype suit manufacturing lab... in the year
# 1518! It turns out that having direct access to history is very convenient
# for a group of historians.

# You still have to be careful of time paradoxes, and so it will be important
# to avoid anyone from 1518 while The Historians search for the Chief.
# Unfortunately, a single guard is patrolling this part of the lab.

# Maybe you can work out where the guard will go ahead of time so that The
# Historians can search safely?

# You start by making a map (your puzzle input) of the situation. For example:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#..^.....
# ........#.
# #.........
# ......#...

# The map shows the current position of the guard with ^ (to indicate the
# guard is currently facing up from the perspective of the map). Any
# obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

# Lab guards in 1518 follow a very strict patrol protocol which involves
# repeatedly following these steps:

# - If there is something directly in front of you, turn right 90 degrees.
# - Otherwise, take a step forward.

# Following the above protocol, the guard moves up several times until she
# reaches an obstacle (in this case, a pile of failed suit prototypes):

# ....#.....
# ....^....#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...

# Because there is now an obstacle in front of the guard, she turns right
# before continuing straight in her new facing direction:

# ....#.....
# ........>#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#...

# Reaching another obstacle (a spool of several very long polymers), she
# turns right again and continues downward:

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#......v.
# ........#.
# #.........
# ......#...

# This process continues for a while, but the guard eventually leaves the
# mapped area (after walking past a tank of universal solvent):

# ....#.....
# .........#
# ..........
# ..#.......
# .......#..
# ..........
# .#........
# ........#.
# #.........
# ......#v..

# By predicting the guard's route, you can determine which specific positions
# in the lab will be in the patrol path. Including the guard's starting
# position, the positions visited by the guard before leaving the area are
# marked with an X:

# ....#.....
# ....XXXXX#
# ....X...X.
# ..#.X...X.
# ..XXXXX#X.
# ..X.X.X.X.
# .#XXXXXXX.
# .XXXXXXX#.
# #XXXXXXX..
# ......#X..

# In this example, the guard will visit 41 distinct positions on your map.

# Predict the path of the guard. How many distinct positions will the guard
# visit before leaving the mapped area?

# -------------------
# PART 2: Description
# -------------------

# While The Historians begin working around the guard's patrol route, you
# borrow their fancy device and step outside the lab. From the safety of a
# supply closet, you time travel through the last few months and record the
# nightly status of the lab's guard post on the walls of the closet.

# Returning after what seems like only a few seconds to The Historians, they
# explain that the guard's patrol area is simply too large for them to safely
# search the lab without getting caught.

# Fortunately, they are pretty sure that adding a single new obstruction
# won't cause a time paradox. They'd like to place the new obstruction in
# such a way that the guard will get stuck in a loop, making the rest of the
# lab safe to search.

# To have the lowest chance of creating a time paradox, The Historians would
# like to know all of the possible positions for such an obstruction. The new
# obstruction can't be placed at the guard's starting position - the guard is
# there right now and would notice.

# In the above example, there are only 6 different positions where a new
# obstruction would cause the guard to get stuck in a loop. The diagrams of
# these six situations use O to mark the new obstruction, | to show a
# position where the guard moves up/down, - to show a position where the
# guard moves left/right, and + to show a position where the guard moves both
# up/down and left/right.

# Option one, put a printing press next to the guard's starting position:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ....|..#|.
# ....|...|.
# .#.O^---+.
# ........#.
# #.........
# ......#...

# Option two, put a stack of failed suit prototypes in the bottom right
# quadrant of the mapped area:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ......O.#.
# #.........
# ......#...

# Option three, put a crate of chimney-squeeze prototype fabric next to the
# standing desk in the bottom right quadrant:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----+O#.
# #+----+...
# ......#...

# Option four, put an alchemical retroencabulator near the bottom left
# corner:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ..|...|.#.
# #O+---+...
# ......#...

# Option five, put the alchemical retroencabulator a bit to the right
# instead:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# ....|.|.#.
# #..O+-+...
# ......#...

# Option six, put a tank of sovereign glue right next to the tank of
# universal solvent:

# ....#.....
# ....+---+#
# ....|...|.
# ..#.|...|.
# ..+-+-+#|.
# ..|.|.|.|.
# .#+-^-+-+.
# .+----++#.
# #+----++..
# ......#O..

# It doesn't really matter what you choose to use as an obstacle so long
# as you and The Historians can put it into position without the guard noticing.
# The important thing is having enough options that you can find one that
# minimizes time paradoxes, and in this example, there are 6 different
# positions you could choose.

# You need to get the guard stuck in a loop by adding a single new
# obstruction. How many different positions could you choose for this obstruction?

class DIR(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


Coord: TypeAlias = tuple[int, int]  # (x, y)
Position: TypeAlias = tuple[Coord, int]  # ((x, y), direction)
Grid: TypeAlias = list[list[str]]

directions = [
    (0, -1),  # up
    (1, 0),  # right
    (0, 1),  # down
    (-1, 0)  # left
]


def find_start_position(grid: Grid) -> Position:
    for y, row in enumerate(grid):
        try:
            x = row.index('^')
            return (x, y), DIR.UP.value
        except ValueError:
            continue
    raise ValueError("There is no starting point")


def out_of_bounds(coord: Coord, grid: Grid) -> bool:
    x, y = coord
    x_out = x < 0 or len(grid[0]) <= x
    y_out = y < 0 or len(grid) <= y
    return x_out or y_out


def is_obstacle(coord: Coord, grid: Grid) -> bool:
    x, y = coord
    return grid[y][x] == '#'


def step(pos: Position) -> Position:
    (x, y), direction = pos
    dx, dy = directions[direction]
    return (x + dx, y + dy), direction


def turn(pos: Position) -> Position:
    coord, direction = pos
    return coord, (direction + 1) % 4


def find_path(grid: Grid, start_pos: Position) -> list[Position]:
    path = [start_pos]

    curr_pos = start_pos
    while True:
        next_pos = step(curr_pos)
        next_coord = next_pos[0]
        if out_of_bounds(next_coord, grid):
            break

        if is_obstacle(next_coord, grid):
            next_pos = turn(curr_pos)
        path.append(next_pos)
        curr_pos = next_pos

    return path


def path_loops(grid: Grid, obstacle: Coord, start_pos: Position, previous_corners: Set[Position]) -> bool:
    visited_corners = previous_corners.copy()

    curr_pos = start_pos
    corner_to_add: Position | None = None

    while True:
        if curr_pos in visited_corners:
            return True
        if corner_to_add:
            visited_corners.add(corner_to_add)
            corner_to_add = None

        next_pos = step(curr_pos)
        next_coord = next_pos[0]
        if out_of_bounds(next_coord, grid):
            return False

        if is_obstacle(next_coord, grid) or next_coord == obstacle:
            next_pos = turn(curr_pos)
            corner_to_add = next_pos
        curr_pos = next_pos


class Day6(AocSolution):

    @property
    def title(self) -> str:
        return "Guard Gallivant"

    @property
    def question_part1(self) -> str:
        return "How many distinct positions will the guard visit before leaving the mapped area?"

    @property
    def question_part2(self) -> str:
        return "How many different positions could you choose for this obstruction?"

    @solution(4758)
    def solve_part1(self, input_data: InputSource) -> int:
        grid = input_data.read_char_grid()

        start = find_start_position(grid)
        path = find_path(grid, start)

        distinct_coords = set([pos[0] for pos in path])
        return len(distinct_coords)

    @solution(1670)
    def solve_part2(self, input_data: InputSource) -> int:
        grid = input_data.read_char_grid()

        start_pos = find_start_position(grid)
        path = find_path(grid, start_pos)

        possible_obstacles = set()
        total_positions = len(path)
        loops_found = 0

        progress = self.create_progress(total_positions, 'Searching for loops')

        visited_corners: Set[Position] = set()
        tested_coords: Set[Coord] = set()
        curr_pos = start_pos
        corner_to_add: Position | None = None
        for next_pos in path[1:]:
            progress.update()

            obstacle, next_dir = next_pos
            if obstacle in tested_coords:
                continue

            if path_loops(grid, obstacle, curr_pos, visited_corners):
                loops_found += 1
                possible_obstacles.add(obstacle)

            tested_coords.add(obstacle)

            if corner_to_add:
                visited_corners.add(corner_to_add)
                corner_to_add = None

            if next_dir != curr_pos[1]:
                corner_to_add = next_pos

            curr_pos = next_pos

        progress.finish()
        return loops_found


if __name__ == "__main__":
    solution = Day6()

    # Run with example data in debug mode
    # solution.run(part=1, is_example=True, debug=True)

    # Run both parts with real input
    solution.run(is_example=False)
