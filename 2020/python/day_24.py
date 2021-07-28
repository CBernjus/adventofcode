# ----------------------------
# Advent of Code 2020 - Day 24
# Part 1: Lobby Layout
# ----------------------------

# Your raft makes it to the tropical island; it turns out that the small crab
# was an excellent navigator. You make your way to the resort.

# As you enter the lobby, you discover a small problem: the floor is being
# renovated. You can't even reach the check-in desk until they've finished
# installing the new tile floor.

# The tiles are all hexagonal; they need to be arranged in a hex grid with a
# very specific color pattern. Not in the mood to wait, you offer to help
# figure out the pattern.

# The tiles are all white on one side and black on the other. They start with
# the white side facing up. The lobby is large enough to fit whatever pattern
# might need to appear there.

# A member of the renovation crew gives you a list of the tiles that need to
# be flipped over (your puzzle input). Each line in the list identifies a
# single tile that needs to be flipped by giving a series of steps starting
# from a reference tile in the very center of the room. (Every line starts
# from the same reference tile.)

# Because the tiles are hexagonal, every tile has six neighbors: east,
# southeast, southwest, west, northwest, and northeast. These directions are
# given in your list, respectively, as e, se, sw, w, nw, and ne. A tile is
# identified by a series of these directions with no delimiters; for example,
# esenee identifies the tile you land on if you start at the reference tile
# and then move one tile east, one tile southeast, one tile northeast, and
# one tile east.

# Each time a tile is identified, it flips from white to black or from black
# to white. Tiles might be flipped more than once. For example, a line like
# esew flips a tile immediately adjacent to the reference tile, and a line
# like nwwswee flips the reference tile itself.

# Here is a larger example:

# sesenwnenenewseeswwswswwnenewsewsw
# neeenesenwnwwswnenewnwwsewnenwseswesw
# seswneswswsenwwnwse
# nwnwneseeswswnenewneswwnewseswneseene
# swweswneswnenwsewnwneneseenw
# eesenwseswswnenwswnwnwsewwnwsene
# sewnenenenesenwsewnenwwwse
# wenwwweseeeweswwwnwwe
# wsweesenenewnwwnwsenewsenwwsesesenwne
# neeswseenwwswnwswswnw
# nenwswwsewswnenenewsenwsenwnesesenew
# enewnwewneswsewnwswenweswnenwsenwsw
# sweneswneswneneenwnewenewwneswswnese
# swwesenesewenwneswnwwneseswwne
# enesenwswwswneneswsenwnewswseenwsese
# wnwnesenesenenwwnenwsewesewsesesew
# nenewswnwewswnenesenwnesewesw
# eneswnwswnwsenenwnwnwwseeswneewsenese
# neswnwewnwnwseenwseesewsenwsweewe
# wseweeenwnesenwwwswnew

# In the above example, 10 tiles are flipped once (to black), and 5 more are
# flipped twice (to black, then back to white). After all of these
# instructions have been followed, a total of 10 tiles are black.

# Go through the renovation crew's list and determine which tiles they need
# to flip. After all of the instructions have been followed, how many tiles
# are left with the black side up?

import os
from typing import Dict, List, Tuple, Set
from collections import Counter

DIRECTIONS = {'w': (-1, 0), 'nw': (0, 1), 'ne': (1, 1),
              'e': (1, 0), 'se': (0, -1), 'sw': (-1, -1)}


def read_instructions(f) -> List[List[str]]:
    lines = f.read().split('\n')
    tiles = []
    for line in lines:
        tile = []
        chars = [c for c in line]
        i = 0
        while i < len(line):
            c = chars.pop(0)
            i += 1
            if c == 's' or c == 'n':
                c += chars.pop(0)
                i += 1
            tile.append(c)
        tiles.append(tile)
    return tiles


def init_board(instructions: List[List[str]]) -> Set[Tuple[int, int]]:
    coords = list(map(calc_coords, instructions))
    black_tiles = set()
    for coord in coords:
        black_tiles = flip_tile(coord, black_tiles)
    return black_tiles


def calc_coords(instruction: List[str]) -> Tuple[int, int]:
    x = 0
    y = 0
    for instr in instruction:
        dx, dy = DIRECTIONS[instr]
        x += dx
        y += dy
    return (x, y)


def flip_tile(tile: Tuple[int, int], black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    if tile in black_tiles:
        black_tiles.remove(tile)
    else:
        black_tiles.add(tile)
    return black_tiles


# with open(os.path.dirname(__file__) + "/../examples/example_24.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_24.txt") as f:
    instructions = read_instructions(f)
    black_tiles = init_board(instructions)

    print("2020 - Day 24 - Part 1")
    print(len(black_tiles))
    # => 420
    #    ===


# ----------------------------
# Advent of Code 2020 - Day 24
# Part 2: Lobby Layout
# ----------------------------

# The tile floor in the lobby is meant to be a living art exhibit. Every day,
# the tiles are all flipped according to the following rules:

#   - Any black tile with zero or more than 2 black tiles immediately
#     adjacent to it is flipped to white.
#   - Any white tile with exactly 2 black tiles immediately adjacent to it
#     is flipped to black.

# Here, tiles immediately adjacent means the six tiles directly touching the
# tile in question.

# The rules are applied simultaneously to every tile; put another way, it is
# first determined which tiles need to be flipped, then they are all flipped
# at the same time.

# In the above example, the number of black tiles that are facing up after
# the given number of days has passed is as follows:

# Day 1: 15
# Day 2: 12
# Day 3: 25
# Day 4: 14
# Day 5: 23
# Day 6: 28
# Day 7: 41
# Day 8: 37
# Day 9: 49
# Day 10: 37

# Day 20: 132
# Day 30: 259
# Day 40: 406
# Day 50: 566
# Day 60: 788
# Day 70: 1106
# Day 80: 1373
# Day 90: 1844
# Day 100: 2208

# After executing this process a total of 100 times, there would be 2208
# black tiles facing up.

DAYS_TO_SIMULATE = 100


def get_neighbors(tile: Tuple[int, int]) -> List[Tuple[int, int]]:
    return [(tile[0] + dir[0], tile[1] + dir[1]) for dir in DIRECTIONS.values()]


def count_black_neighbors(tile: Tuple[int, int], black_tiles: Set[Tuple[int, int]]) -> int:
    count = 0
    black = []
    for neighbor in get_neighbors(tile):
        if neighbor in black_tiles:
            black.append(neighbor)
        count += 1 if neighbor in black_tiles else 0
    return count


def tile_flips(tile: Tuple[int, int], black_tiles: Set[Tuple[int, int]]) -> bool:
    neighbors = count_black_neighbors(tile, black_tiles)
    if tile in black_tiles:
        return True if neighbors == 0 or neighbors > 2 else False
    else:
        return True if neighbors == 2 else False


def simulate_day(black_tiles: Set[Tuple[int, int]]) -> Set[Tuple[int, int]]:
    flipping = set()
    for tile in black_tiles:
        neighbors = get_neighbors(tile)
        if tile_flips(tile, black_tiles):
            flipping.add(tile)
        for neighbor in neighbors:
            if tile_flips(neighbor, black_tiles):
                flipping.add(neighbor)

    for tile in flipping:
        black_tiles = flip_tile(tile, black_tiles)
    return black_tiles


# with open(os.path.dirname(__file__) + "/../examples/example_24.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_24.txt") as f:
    instructions = read_instructions(f)
    black_tiles = init_board(instructions)

    print("2020 - Day 24 - Part 2")
    for day in range(DAYS_TO_SIMULATE):
        # print('Day ' + str(day) + ':', len(black_tiles))
        black_tiles = simulate_day(black_tiles)

    print('Day ' + str(DAYS_TO_SIMULATE) + ':', len(black_tiles))
    # => 4206
    #    ====
