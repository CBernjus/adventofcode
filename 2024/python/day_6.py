import logging
import os
import shutil
from collections import deque
from sys import stdout

# logging.basicConfig(level=logging.DEBUG)

DAY = 6
# ---------------------------
# Advent of Code 2024 - Day 6
# Part 1: Guard Gallivant
# ---------------------------

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

Position = tuple[int, int, str]

directions = {
    'up': (0, -1, 'right'),
    'right': (1, 0, 'down'),
    'down': (0, 1, 'left'),
    'left': (-1, 0, 'up')
}


def find_start_coordinates(grid: list[str]) -> Position:
    start = None
    for y, row in enumerate(grid):
        try:
            x = row.index('^')
        except ValueError:
            continue
        start = (x, y, 'up')

    if not start:
        raise ValueError("There is no starting point")

    return start


def get_next_coordinate(pos: Position, direction: str) -> Position:
    if direction not in directions.keys():
        raise ValueError("The given direction must be valid")
    x, y, _ = pos
    logging.debug(f'curr: {pos}')
    dx, dy, next_dir = directions[direction]
    logging.debug(f'dir: {direction}, {dx, dy}')
    logging.debug(f'next: {x + dx, y + dy}')
    return x + dx, y + dy, direction


def out_of_bounds(pos: Position, grid: list[str]) -> bool:
    x, y, _ = pos
    return x < 0 or x >= len(grid[0]) or y < 0 or y >= len(grid)


def is_obstacle(pos: Position, grid: list[str]) -> bool:
    x, y, _ = pos
    return grid[y][x] == '#'


def find_path(grid: list[str], start: Position) -> list[Position]:
    path = [start]

    curr_dir = 'up'
    curr_pos = start
    while True:
        next_pos = get_next_coordinate(curr_pos, curr_dir)
        if out_of_bounds(next_pos, grid):
            break

        if is_obstacle(next_pos, grid):
            # rotate
            logging.debug('obstacle -> rotate')
            _, _, next_dir = directions[curr_dir]
            curr_dir = next_dir
        else:
            # step forward
            logging.debug('step forward')
            path.append(next_pos)
            curr_pos = next_pos
        logging.debug('')

    return path


# with open(os.path.dirname(__file__) + f"/../examples/example_{DAY}.txt") as f:
with open(os.path.dirname(__file__) + f"/../inputs/input_{DAY}.txt") as f:
    grid = [line.strip() for line in f.readlines()]

    start = find_start_coordinates(grid)
    # path = find_path(grid, start)

    # count_distinct_pos = len(set(path))

    print(f"2024 - Day {DAY} - Part 1")
    print("How many distinct positions will the guard visit before leaving the mapped area?")
    # print(count_distinct_pos)
    # => 4758
    #    =======

print()


# ---------------------------
# Advent of Code 2024 - Day 6
# Part 2: Guard Gallivant
# ---------------------------

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

def could_reach(pos_from: Position, pos_to: Position, direction: str, grid: list[str]) -> bool:
    if pos_from[0] != pos_to[0] and pos_from[1] != pos_to[1]:
        return False

    logging.debug(f'search for: {pos_to} in dir "{direction}" from {pos_from}')
    while pos_from != pos_to:
        if is_obstacle(pos_from, grid):
            return False
        pos_from = get_next_coordinate(pos_from, direction)
    return True


def possible_obstacle_ahead(curr_pos: Position, turns: deque, grid: list[str]) -> bool:
    if len(turns) < 3:
        return False
    for i in range(len(turns) - 3):
        turn, direction = turns[i]
        if not could_reach(curr_pos, turn, direction, grid):
            return False
    return True


def find_possible_obstacles(grid: list[str], start: Position) -> set[Position]:
    obstacles = set()
    turns = deque()

    curr_dir = 'up'
    curr_pos = start
    next_pos = get_next_coordinate(curr_pos, curr_dir)
    while True:
        if out_of_bounds(next_pos, grid):
            break
        if is_obstacle(next_pos, grid):
            # rotate
            logging.debug('obstacle -> rotate')
            turns.append((curr_pos, curr_dir))
            _, _, next_dir = directions[curr_dir]
            curr_dir = next_dir
        else:
            # step forward
            if possible_obstacle_ahead(curr_pos, turns, grid):
                obstacles.add(next_pos)
                logging.debug(f'FOUND obstacle: {next_pos}')
            logging.debug('step forward')
            curr_pos = next_pos
        logging.debug('')
        next_pos = get_next_coordinate(curr_pos, curr_dir)

    return obstacles


def path_loops(grid: list[str], start: Position) -> bool:
    visited_states = set(start)

    curr_dir = 'up'
    curr_pos = start

    while True:
        state = (curr_pos[0], curr_pos[1], curr_dir)
        if state in visited_states:
            return True

        next_pos = get_next_coordinate(curr_pos, curr_dir)

        if out_of_bounds(next_pos, grid):
            return False

        if is_obstacle(next_pos, grid):
            # rotate
            _, _, next_dir = directions[curr_dir]
            curr_dir = next_dir
        else:
            # step forward
            visited_states.add(state)
            curr_pos = next_pos

    return False


def modify_grid(grid: list[str], pos: Position) -> list[str]:
    modified = grid[:]
    x, y, _ = pos
    line = modified[y]
    modified[y] = line[:x] + '#' + line[x + 1:]
    return modified


def format_progress(current, total, position, loops_found):
    percentage = (current / total) * 100
    # Get terminal width for proper clearing
    terminal_width = shutil.get_terminal_size().columns
    # Format the progress message
    message = f'Testing {current}/{total} ({percentage:.1f}%): {position} | Loops found: {loops_found}'
    # Pad with spaces to clear the line completely, but put \r at the start
    return '\r' + message.ljust(terminal_width - 1)  # -1 to account for \r


# with open(os.path.dirname(__file__) + f"/../examples/example_{DAY}.txt") as f:
with open(os.path.dirname(__file__) + f"/../inputs/input_{DAY}.txt") as f:
    print(f"2024 - Day {DAY} - Part 2")

    grid = [line.strip() for line in f.readlines()]

    start = find_start_coordinates(grid)
    path = find_path(grid, start)
    print(f'path length: {len(path)}')

    unique_positions = set([(x, y) for x, y, _ in path])
    print(f'unique: {len(unique_positions)}')

    possible_obstacles = set()
    total_positions = len(path)
    loops_found = 0

    for idx, position in enumerate(path, 1):
        x, y, _ = position
        if (x, y) in possible_obstacles:
            continue

        # update progress
        stdout.write(format_progress(idx, total_positions, position, loops_found))
        stdout.flush()

        # modify grid and simulate
        modified_grid = modify_grid(grid, position)
        if path_loops(modified_grid, start):
            loops_found += 1
            possible_obstacles.add((x, y))

    stdout.write('\n')

    print("How many different positions could you choose for this obstruction?")
    print(len(possible_obstacles))
    # => 1670
    #    ==========
