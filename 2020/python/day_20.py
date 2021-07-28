# ----------------------------
# Advent of Code 2020 - Day 20
# Part 1: Jurassic Jigsaw
# ----------------------------

# The high-speed train leaves the forest and quickly carries you south. You
# can even see a desert in the distance! Since you have some spare time, you
# might as well see if there was anything interesting in the image the
# Mythical Information Bureau satellite captured.

# After decoding the satellite messages, you discover that the data actually
# contains many small images created by the satellite's camera array. The
# camera array consists of many cameras; rather than produce a single square
# image, they produce many smaller square image tiles that need to be
# reassembled back into a single image.

# Each camera in the camera array returns a single monochrome image tile with
# a random unique ID number. The tiles (your puzzle input) arrived in a
# random order.

# Worse yet, the camera array appears to be malfunctioning: each image tile
# has been rotated and flipped to a random orientation. Your first task is to
# reassemble the original image by orienting the tiles so they fit together.

# To show how the tiles should be reassembled, each tile's image data
# includes a border that should line up exactly with its adjacent tiles. All
# tiles have this border, and the border lines up exactly when the tiles are
# both oriented correctly. Tiles at the edge of the image also have this
# border, but the outermost edges won't line up with any other tiles.

# For example, suppose you have the following nine tiles:

# Tile 2311:
# ..##.#..#.
# ##..#.....
# #...##..#.
# ####.#...#
# ##.##.###.
# ##...#.###
# .#.#.#..##
# ..#....#..
# ###...#.#.
# ..###..###

# Tile 1951:
# #.##...##.
# #.####...#
# .....#..##
# #...######
# .##.#....#
# .###.#####
# ###.##.##.
# .###....#.
# ..#.#..#.#
# #...##.#..

# Tile 1171:
# ####...##.
# #..##.#..#
# ##.#..#.#.
# .###.####.
# ..###.####
# .##....##.
# .#...####.
# #.##.####.
# ####..#...
# .....##...

# Tile 1427:
# ###.##.#..
# .#..#.##..
# .#.##.#..#
# #.#.#.##.#
# ....#...##
# ...##..##.
# ...#.#####
# .#.####.#.
# ..#..###.#
# ..##.#..#.

# Tile 1489:
# ##.#.#....
# ..##...#..
# .##..##...
# ..#...#...
# #####...#.
# #..#.#.#.#
# ...#.#.#..
# ##.#...##.
# ..##.##.##
# ###.##.#..

# Tile 2473:
# #....####.
# #..#.##...
# #.##..#...
# ######.#.#
# .#...#.#.#
# .#########
# .###.#..#.
# ########.#
# ##...##.#.
# ..###.#.#.

# Tile 2971:
# ..#.#....#
# #...###...
# #.#.###...
# ##.##..#..
# .#####..##
# .#..####.#
# #..#.#..#.
# ..####.###
# ..#.#.###.
# ...#.#.#.#

# Tile 2729:
# ...#.#.#.#
# ####.#....
# ..#.#.....
# ....#..#.#
# .##..##.#.
# .#.####...
# ####.#.#..
# ##.####...
# ##..#.##..
# #.##...##.

# Tile 3079:
# #.#.#####.
# .#..######
# ..#.......
# ######....
# ####.#..#.
# .#...#.##.
# #.#####.##
# ..#.###...
# ..#.......
# ..#.###...

# By rotating, flipping, and rearranging them, you can find a square
# arrangement that causes all adjacent borders to line up:

# #...##.#.. ..###..### #.#.#####.
# ..#.#..#.# ###...#.#. .#..######
# .###....#. ..#....#.. ..#.......
# ###.##.##. .#.#.#..## ######....
# .###.##### ##...#.### ####.#..#.
# .##.#....# ##.##.###. .#...#.##.
# #...###### ####.#...# #.#####.##
# .....#..## #...##..#. ..#.###...
# #.####...# ##..#..... ..#.......
# #.##...##. ..##.#..#. ..#.###...

# #.##...##. ..##.#..#. ..#.###...
# ##..#.##.. ..#..###.# ##.##....#
# ##.####... .#.####.#. ..#.###..#
# ####.#.#.. ...#.##### ###.#..###
# .#.####... ...##..##. .######.##
# .##..##.#. ....#...## #.#.#.#...
# ....#..#.# #.#.#.##.# #.###.###.
# ..#.#..... .#.##.#..# #.###.##..
# ####.#.... .#..#.##.. .######...
# ...#.#.#.# ###.##.#.. .##...####

# ...#.#.#.# ###.##.#.. .##...####
# ..#.#.###. ..##.##.## #..#.##..#
# ..####.### ##.#...##. .#.#..#.##
# #..#.#..#. ...#.#.#.. .####.###.
# .#..####.# #..#.#.#.# ####.###..
# .#####..## #####...#. .##....##.
# ##.##..#.. ..#...#... .####...#.
# #.#.###... .##..##... .####.##.#
# #...###... ..##...#.. ...#..####
# ..#.#....# ##.#.#.... ...##.....

# For reference, the IDs of the above tiles are:

# 1951    2311    3079
# 2729    1427    2473
# 2971    1489    1171

# To check that you've assembled the image correctly, multiply the IDs of the
# four corner tiles together. If you do this with the assembled tiles from
# the example above, you get 1951 * 3079 * 2971 * 1171 = 20899048083289.

# Assemble the tiles into an image. What do you get if you multiply together
# the IDs of the four corner tiles?

from __future__ import annotations
import os
import re
import math
import time
from typing import List, Tuple
from collections import Counter


def rotate(cells: List[str]) -> List[str]:
    list_of_tuples = zip(*cells[::-1])
    return [''.join(list(elem)) for elem in list_of_tuples]


def flip(cells: List[str]) -> List[str]:
    return list(map(lambda row: row[::-1], cells))


class Tile:
    id: int
    cells: List[str]
    border_ids: List[int]
    degree: int

    def __init__(self, id: int, cells: List[str], border_ids=[], degree=0):
        self.id = id
        self.cells = cells
        self.border_ids = border_ids
        if len(self.border_ids) != 8:
            self.border_ids = self.generate_border_ids()
        self.degree = degree

    def rotate(self):
        self.cells = rotate(self.cells)
        self.border_ids = self.border_ids[6:] + self.border_ids[:6]

    def flip(self):
        self.cells = flip(self.cells)
        self.border_ids = self.border_ids[1::-1] + self.border_ids[7:5:-1] + \
            self.border_ids[5:3:-1] + self.border_ids[3:1:-1]

    def generate_border_ids(self):
        # Generate Border IDs
        border_ids = []
        for _ in range(4):
            self.rotate()
            border_ids.append(int(self.cells[0], 2))
            border_ids.append(int(self.cells[0][::-1], 2))
        return border_ids

    def calculate_degree(self, counter_of_all_border_ids: List[int]):
        degree = 0
        for border_id in self.border_ids:
            if counter_of_all_border_ids[border_id] > 1:
                degree += 1
        self.degree = degree // 2

    def can_link_below(self, b: Tile) -> bool:
        # return self.border_ids[4] == b.border_ids[1]
        return self.cells[-1] == b.cells[0]

    def can_link_right(self, b: Tile) -> bool:
        # return self.border_ids[6] == b.border_ids[3]
        for i in range(len(self.cells)):
            if self.cells[i][-1] != b.cells[i][0]:
                return False
        return True

    def get_image(self) -> List[str]:
        image = []
        for i in range(1, len(self.cells) - 1):
            image.append(
                self.cells[i][1:-1].replace('0', '.').replace('1', '#'))
        return image

    def __str__(self):
        return f"{self.id}: {self.border_ids}, {self.degree}, {self.cells}"

    def __copy__(self) -> Tile:
        return Tile(self.id, self.cells, self.border_ids, self.degree)


def read_tiles(f) -> List[Tile]:
    regex = r"Tile (?P<id>\d+):\n(?P<tile>(?:[01]+\n)+)"
    input = f.read().replace('.', '0').replace('#', '1')
    matches = re.finditer(regex, input)
    tiles = []
    for match in matches:
        (id, cells) = match.groups()
        tiles.append(Tile(int(id), cells.split('\n')[:-1]))

    return tiles


def calculate_degrees(tiles: List[List[str]]) -> List[Tuple[str, int]]:
    possible_border_ids = [id for ids in map(
        lambda tile: tile.border_ids, tiles) for id in ids]
    counter = Counter(possible_border_ids)
    degrees = []

    for tile in tiles:
        tile.calculate_degree(counter)
        degrees.append((tile.id, tile.degree))

    return degrees


def find_corner_tile_ids_by_degree(tiles: List[List[str]]) -> List[int]:
    degrees = calculate_degrees(tiles)
    return list(map(lambda d: int(d[0]), filter(lambda d: d[1] == 2, degrees)))


def prod(numbers: List[int]) -> int:
    prod = 1
    for x in numbers:
        prod *= x
    return prod


# with open(os.path.dirname(__file__) + "/../examples/example_20.txt") as f:
with open(os.path.dirname(__file__) + "/../examples/example_20.txt") as f:
    tiles = read_tiles(f)
    print("2020 - Day 20 - Part 1")
    corners = find_corner_tile_ids_by_degree(tiles)
    print('corners:', corners)
    print('prod:', prod(corners))
    # => 27798062994017
    #    ==============


# ----------------------------
# Advent of Code 2020 - Day 20
# Part 2: Jurassic Jigsaw
# ----------------------------

# Now, you're ready to check the image for sea monsters.

# The borders of each tile are not part of the actual image; start by
# removing them.

# In the example above, the tiles become:

# .#.#..#. ##...#.# #..#####
# ###....# .#....#. .#......
# ##.##.## #.#.#..# #####...
# ###.#### #...#.## ###.#..#
# ##.#.... #.##.### #...#.##
# ...##### ###.#... .#####.#
# ....#..# ...##..# .#.###..
# .####... #..#.... .#......

# #..#.##. .#..###. #.##....
# #.####.. #.####.# .#.###..
# ###.#.#. ..#.#### ##.#..##
# #.####.. ..##..## ######.#
# ##..##.# ...#...# .#.#.#..
# ...#..#. .#.#.##. .###.###
# .#.#.... #.##.#.. .###.##.
# ###.#... #..#.##. ######..

# .#.#.### .##.##.# ..#.##..
# .####.## #.#...## #.#..#.#
# ..#.#..# ..#.#.#. ####.###
# #..####. ..#.#.#. ###.###.
# #####..# ####...# ##....##
# #.##..#. .#...#.. ####...#
# .#.###.. ##..##.. ####.##.
# ...###.. .##...#. ..#..###

# Remove the gaps to form the actual image:

# .#.#..#.##...#.##..#####
# ###....#.#....#..#......
# ##.##.###.#.#..######...
# ###.#####...#.#####.#..#
# ##.#....#.##.####...#.##
# ...########.#....#####.#
# ....#..#...##..#.#.###..
# .####...#..#.....#......
# #..#.##..#..###.#.##....
# #.####..#.####.#.#.###..
# ###.#.#...#.######.#..##
# #.####....##..########.#
# ##..##.#...#...#.#.#.#..
# ...#..#..#.#.##..###.###
# .#.#....#.##.#...###.##.
# ###.#...#..#.##.######..
# .#.#.###.##.##.#..#.##..
# .####.###.#...###.#..#.#
# ..#.#..#..#.#.#.####.###
# #..####...#.#.#.###.###.
# #####..#####...###....##
# #.##..#..#...#..####...#
# .#.###..##..##..####.##.
# ...###...##...#...#..###

# Now, you're ready to search for sea monsters! Because your image is
# monochrome, a sea monster will look like this:

#                   #
# #    ##    ##    ###
#  #  #  #  #  #  #

# When looking for this pattern in the image, the spaces can be anything;
# only the # need to match. Also, you might need to rotate or flip your image
# before it's oriented correctly to find sea monsters. In the above image,
# after flipping and rotating it to the appropriate orientation, there are
# two sea monsters (marked with O):

# .####...#####..#...###..
# #####..#..#.#.####..#.#.
# .#.#...#.###...#.##.O#..
# #.O.##.OO#.#.OO.##.OOO##
# ..#O.#O#.O##O..O.#O##.##
# ...#.#..##.##...#..#..##
# #.##.#..#.#..#..##.#.#..
# .###.##.....#...###.#...
# #.####.#.#....##.#..#.#.
# ##...#..#....#..#...####
# ..#.##...###..#.#####..#
# ....#.##.#.#####....#...
# ..##.##.###.....#.##..#.
# #...#...###..####....##.
# .#.##...#.##.#.#.###...#
# #.###.#..####...##..#...
# #.###...#.##...#.##O###.
# .O##.#OO.###OO##..OOO##.
# ..O#.O..O..O.#O##O##.###
# #.#..##.########..#..##.
# #.#####..#.#...##..#....
# #....##..#.#########..##
# #...#.....#..##...###.##
# #..###....##.#...##.##.#

# Determine how rough the waters are in the sea monsters' habitat by counting
# the number of # that are not part of a sea monster. In the above example,
# the habitat's water roughness is 273.

# How many # are not part of a sea monster?


def get_permutations(tiles: List[Tile]) -> List[Tile]:
    permutations = []
    for tile in tiles:
        for _ in range(2):
            for _ in range(4):
                permutations.append(tile.__copy__())
                tile.rotate()
            tile.flip()
    return permutations


def search(permutations: List[Tile], row: int, col: int, grid_size: int, visited: List[int], grid: List[List[Tile]]) -> List[List[Tile]]:
    if row == grid_size:
        return (True, grid)
    for tile in permutations:
        if tile.id not in visited:
            if row > 0 and not grid[row-1][col].can_link_below(tile):
                continue
            if col > 0 and not grid[row][col-1].can_link_right(tile):
                continue
            grid[row][col] = tile
            visited.append(tile.id)
            if col == grid_size - 1:
                found, newGrid = search(permutations, row + 1, 0,
                                        grid_size, visited, grid)
            else:
                found, newGrid = search(permutations, row, col + 1,
                                        grid_size, visited, grid)
            if found:
                return (found, newGrid)
            visited.remove(tile.id)

    return (False, None)


def build_grid(tiles: List[Tile]):
    permutations = get_permutations(tiles)
    grid_size = round(math.sqrt(len(tiles)))
    grid = [[None] * grid_size for _ in range(grid_size)]
    _, grid = search(permutations, 0, 0, grid_size, [], grid)
    return grid


def build_image(grid: List[List[Tile]]) -> List[str]:
    image = []
    for grid_row in grid:
        list_of_tuples = zip(*[tile.get_image() for tile in grid_row])
        row = [''.join(list(elem)) for elem in list_of_tuples]
        for line in row:
            image.append(line)
    return image


def populate_monsters(sea: List[str], monster: List[str]) -> List[str]:
    h = len(monster)
    w = len(monster[0])
    n = len(sea)
    orientation_found = False
    for _ in range(2):
        for _ in range(4):
            for row in range(0, n - h):
                for col in range(0, n - w):
                    can_be = True
                    for r in range(0, h):
                        for c in range(0, w):
                            if monster[r][c] == '#' and sea[row+r][col+c] == '.':
                                can_be = False
                                break
                    if not can_be:
                        continue
                    orientation_found = True

                    for r in range(0, h):
                        modified_row = sea[row+r][:col]
                        for c in range(0, w):
                            if monster[r][c] == '#':
                                modified_row += 'O'
                            else:
                                modified_row += sea[row+r][col+c]
                        sea[row+r] = modified_row + sea[row+r][col+w:]
            if orientation_found:
                break
            sea = rotate(sea)
        if orientation_found:
            break
        sea = flip(sea)

    return sea


def calculate_sea_roughness(sea: List[str]) -> int:
    return ''.join(sea).count('#')


monster_image = ["                  # ",
                 "#    ##    ##    ###",
                 " #  #  #  #  #  #   "]


# with open(os.path.dirname(__file__) + "/../examples/example_20.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_20.txt") as f:
    print()
    tiles = read_tiles(f)
    grid = build_grid(tiles)
    corners = [grid[0][0].id, grid[0][-1].id, grid[-1][0].id, grid[-1][-1].id]
    print(corners, prod(corners))
    sea_image = build_image(grid)
    sea = populate_monsters(sea_image, monster_image)
    roughness = calculate_sea_roughness(sea)
    print("2020 - Day 20 - Part 2")
    for line in sea:
        print(line.replace('#', '.'))
    print('sea roughness:', roughness)
    # => 2366
    #    ====
