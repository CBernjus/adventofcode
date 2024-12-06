import re
from itertools import product

DAY = 4
# ---------------------------
# Advent of Code 2024 - Day 4
# Part 1: Ceres Search
# ---------------------------

# "Looks like the Chief's not here. Next!" One of The Historians pulls out a
# device and pushes the only button on it. After a brief flash, you recognize
# the interior of the Ceres monitoring station!

# As the search for the Chief continues, a small Elf who lives on the station
# tugs on your shirt; she'd like to know if you could help her with her word
# search (your puzzle input). She only has to find one word: XMAS.

# This word search allows words to be horizontal, vertical, diagonal, written
# backwards, or even overlapping other words. It's a little unusual, though,
# as you don't merely need to find one instance of XMAS - you need to find
# all of them. Here are a few ways XMAS might appear, where irrelevant
# characters have been replaced with .:

# ..X...
# .SAMX.
# .A..A.
# XMAS.S
# .X....

# The actual word search will be full of letters instead. For example:

# MMMSXXMASM
# MSAMXMSMSA
# AMXSXMAAMM
# MSAMASMSMX
# XMASAMXAMM
# XXAMMXXAMA
# SMSMSASXSS
# SAXAMASAAA
# MAMMMXMMMM
# MXMXAXMASX

# In this word search, XMAS occurs a total of 18 times; here's the same word
# search again, but where letters not involved in any XMAS have been replaced
# with .:

# ....XXMAS.
# .SAMXMS...
# ...S..A...
# ..A.A.MS.X
# XMASAMX.MM
# X.....XA.A
# S.S.S.S.SS
# .A.A.A.A.A
# ..M.M.M.MM
# .X.X.XMASX

# Take a look at the little Elf's word search. How many times does XMAS appear?

import os


def extract_diagonal(rows: list[str], start_x: int, start_y: int, dx: int, dy: int) -> str:
    """Extract a single diagonal starting from (start_x, start_y) with direction (dx, dy)."""
    diagonal = []
    x, y = start_x, start_y
    while 0 <= x < len(rows[0]) and 0 <= y < len(rows):
        diagonal.append(rows[y][x])
        x += dx
        y += dy
    return ''.join(diagonal)


def get_diagonals_left(rows, cols):
    """Extract top-left to bottom-right diagonals."""
    diagonals = []
    # Diagonals starting from the first row
    for x in range(len(cols)):
        diagonals.append(extract_diagonal(rows, x, 0, 1, 1))
    # Diagonals starting from the first column
    for y in range(1, len(rows)):
        diagonals.append(extract_diagonal(rows, 0, y, 1, 1))
    return diagonals


def get_diagonals_right(rows, cols):
    """Extract bottom-left to top-right diagonals."""
    diagonals = []
    # Diagonals starting from the last row
    for x in range(len(cols)):
        diagonals.append(extract_diagonal(rows, x, len(rows) - 1, 1, -1))
    # Diagonals starting from the first column
    for y in range(1, len(rows) - 1):
        diagonals.append(extract_diagonal(rows, 0, y, 1, -1))
    return diagonals


def count_pattern_in_all_directions(rows, cols, pattern):
    """Count occurrences of the given pattern in all directions."""
    horizontal = '-'.join(rows)
    vertical = '-'.join(cols)
    diagonals_left = '-'.join(get_diagonals_left(rows, cols))
    diagonals_right = '-'.join(get_diagonals_right(rows, cols))

    all_directions = '-'.join([horizontal, vertical, diagonals_left, diagonals_right])
    return len(re.findall(f"(?={pattern})", all_directions))


# with open(os.path.dirname(__file__) + f"/../examples/example_{DAY}.txt") as f:
with open(os.path.dirname(__file__) + f"/../inputs/input_{DAY}.txt") as f:
    rows = list(map(lambda l: l.strip(), f.readlines()))
    cols = list(map(''.join, zip(*rows)))

    count = count_pattern_in_all_directions(rows, cols, "(?=XMAS|SAMX)")

    print(f"2024 - Day {DAY} - Part 1")
    print("How many times does XMAS appear?")
    print(count)
    # => 2557
    #    =======

print()


# ---------------------------
# Advent of Code 2024 - Day 4
# Part 2: Ceres Search
# ---------------------------

# The Elf looks quizzically at you. Did you misunderstand the assignment?

# Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

# M.S
# .A.
# M.S

# Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

# Here's the same example from before, but this time all of the X-MASes have been kept instead:

# .M.S......
# ..A..MSMS.
# .M.S.MAA..
# ..A.ASMSM.
# .M.S.M....
# ..........
# S.S.S.S.S.
# .A.A.A.A..
# M.M.M.M.M.
# ..........

# In this example, an X-MAS appears 9 times.

# Flip the word search from the instructions back over to the word search
# side and try again. How many times does an X-MAS appear?

def get_coordinates(rows: list[str]) -> list[tuple[int]]:
    return list(product(range(1, len(rows) - 1), range(1, len(rows[0]) - 1)))


def count_x_mas(rows: list[str]) -> int:
    patterns = [
        [(-1, -1, 'M'), (-1, +1, 'M'), (+1, -1, 'S'), (+1, +1, 'S')],  # Ms on left
        [(-1, -1, 'M'), (+1, -1, 'M'), (-1, +1, 'S'), (+1, +1, 'S')],  # Ms above
        [(+1, +1, 'M'), (+1, -1, 'M'), (-1, -1, 'S'), (-1, +1, 'S')],  # Ms on right
        [(+1, +1, 'M'), (-1, +1, 'M'), (-1, -1, 'S'), (+1, -1, 'S')],  # Ms below
    ]

    count = 0
    for x, y in get_coordinates(rows):
        if rows[y][x] != 'A':
            continue
        for pattern in patterns:
            if all(rows[y + dy][x + dx] == char for dx, dy, char in pattern):
                count += 1
    return count


# with open(os.path.dirname(__file__) + f"/../examples/example_{DAY}.txt") as f:
with open(os.path.dirname(__file__) + f"/../inputs/input_{DAY}.txt") as f:
    rows = list(map(lambda l: l.strip(), f.readlines()))

    print(f"2024 - Day {DAY} - Part 2")
    print("How many times does an X-MAS appear?")
    print(count_x_mas(rows))
    # => 1854
    #    ==========
