# ----------------------------
# Advent of Code 2020 - Day 17
# Part 1: Conway Cubes
# ----------------------------

# As your flight slowly drifts through the sky, the Elves at the Mythical
# Information Bureau at the North Pole contact you. They'd like some help
# debugging a malfunctioning experimental energy source aboard one of their
# super-secret imaging satellites.

# The experimental energy source is based on cutting-edge technology: a set
# of Conway Cubes contained in a pocket dimension! When you hear it's having
# problems, you can't help but agree to take a look.

# The pocket dimension contains an infinite 3-dimensional grid. At every
# integer 3-dimensional coordinate (x,y,z), there exists a single cube which
# is either active or inactive.

# In the initial state of the pocket dimension, almost all cubes start
# inactive. The only exception to this is a small flat region of cubes (your
# puzzle input); the cubes in this region start in the specified active (#)
# or inactive (.) state.

# The energy source then proceeds to boot up by executing six cycles.

# Each cube only ever considers its neighbors: any of the 26 other cubes
# where any of their coordinates differ by at most 1. For example, given the
# cube at x=1,y=2,z=3, its neighbors include the cube at x=2,y=2,z=2, the
# cube at x=0,y=2,z=3, and so on.

# During a cycle, all cubes simultaneously change their state according to
# the following rules:

#   - If a cube is active and exactly 2 or 3 of its neighbors are also
#     active, the cube remains active. Otherwise, the cube becomes inactive.
#   - If a cube is inactive but exactly 3 of its neighbors are active, the
#     cube becomes active. Otherwise, the cube remains inactive.

# The engineers responsible for this experimental energy source would like
# you to simulate the pocket dimension and determine what the configuration
# of cubes should be at the end of the six-cycle boot process.

# For example, consider the following initial state:

# .#.
# ..#
# ###

# Even though the pocket dimension is 3-dimensional, this initial state
# represents a small 2-dimensional slice of it. (In particular, this initial
# state defines a 3x3x1 region of the 3-dimensional space.)

# Simulating a few cycles from this initial state produces the following
# configurations, where the result of each cycle is shown layer-by-layer at
# each given z coordinate (and the frame of view follows the active cells in
# each cycle):

# Before any cycles:

# z=0
# .#.
# ..#
# ###


# After 1 cycle:

# z=-1
# #..
# ..#
# .#.

# z=0
# #.#
# .##
# .#.

# z=1
# #..
# ..#
# .#.


# After 2 cycles:

# z=-2
# .....
# .....
# ..#..
# .....
# .....

# z=-1
# ..#..
# .#..#
# ....#
# .#...
# .....

# z=0
# ##...
# ##...
# #....
# ....#
# .###.

# z=1
# ..#..
# .#..#
# ....#
# .#...
# .....

# z=2
# .....
# .....
# ..#..
# .....
# .....


# After 3 cycles:

# z=-2
# .......
# .......
# ..##...
# ..###..
# .......
# .......
# .......

# z=-1
# ..#....
# ...#...
# #......
# .....##
# .#...#.
# ..#.#..
# ...#...

# z=0
# ...#...
# .......
# #......
# .......
# .....##
# .##.#..
# ...#...

# z=1
# ..#....
# ...#...
# #......
# .....##
# .#...#.
# ..#.#..
# ...#...

# z=2
# .......
# .......
# ..##...
# ..###..
# .......
# .......
# .......

# After the full six-cycle boot process completes, 112 cubes are left in the
# active state.

# Starting with your given initial configuration, simulate six cycles. How
# many cubes are left in the active state after the sixth cycle?

import os
from bitarray import bitarray

iterations = 6


class Grid(object):
    bits: bitarray

    def __init__(self, xDim: int, yDim: int, zDim: int, wDim: int = 0):
        self.xDim = xDim
        self.yDim = yDim
        self.zDim = zDim
        self.wDim = wDim
        self.bits = bitarray(xDim * yDim * zDim * wDim)
        self.bits.setall(0)

    def getIndex(self, x: int, y: int, z: int, w: int):
        return w * self.xDim * self.yDim * self.zDim + z * self.xDim * self.yDim + y * self.xDim + x

    def get(self, x: int, y: int, z: int, w: int):
        return self.bits[self.getIndex(x, y, z, w)]

    def set(self, x: int, y: int, z: int, w: int, value: int):
        self.bits[self.getIndex(x, y, z, w)] = value

    def check_rules(self, x: int, y: int, z: int, w: int) -> int:
        activeNeighbors = self.countActiveNeighbors(x, y, z, w)
        if activeNeighbors == 3:
            return 1
        if self.get(x, y, z, w) == 1 and activeNeighbors == 2:
            return 1
        return 0

    def countActiveNeighbors(self, x: int, y: int, z: int, w: int) -> int:
        count = 0

        for dw in [-1, 0, 1]:
            for dz in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        count += self.get(x + dx, y + dy, z + dz, w + dw)

        return count - self.get(x, y, z, w)

    def simulate_cycle(self):
        newGrid = Grid(self.xDim, self.yDim, self.zDim, self.wDim)

        for w in range(1, self.wDim - 1):
            for z in range(1, self.zDim - 1):
                for y in range(1, self.yDim - 1):
                    for x in range(1, self.xDim - 1):
                        newGrid.set(x, y, z, w, self.check_rules(x, y, z, w))

        self.bits = newGrid.bits


def read_input(f):
    lines = f.read().replace('.', '0').replace('#', '1').split('\n')
    xDim = len(lines[0])
    yDim = len(lines)
    return (lines, xDim, yDim)


def read_3d_grid(f, iterations) -> Grid:
    (initLayer, xDim, yDim) = read_input(f)
    padd = iterations + 1

    grid = Grid(xDim + 2 * padd, yDim + 2 * padd, 1 + 2 * padd, 3)

    for i, line in enumerate(initLayer):
        lineStart = grid.getIndex(padd, i + padd, padd, 1)
        grid.bits[lineStart: lineStart + xDim] = bitarray(line)

    return grid


# with open(os.path.dirname(__file__) + "/../examples/example_17.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_17.txt") as f:
    grid = read_3d_grid(f, iterations)
    for i in range(iterations):
        grid.simulate_cycle()
        print("Cycle " + str(i) + " simulated")

    print("2020 - Day 17 - Part 1")
    print(grid.bits.count())
    # => 386
    #    ===


# ----------------------------
# Advent of Code 2020 - Day 17
# Part 2: Conway Cubes
# ----------------------------

# For some reason, your simulated results don't match what the experimental
# energy source engineers expected. Apparently, the pocket dimension actually
# has four spatial dimensions, not three.

# The pocket dimension contains an infinite 4-dimensional grid. At every
# integer 4-dimensional coordinate (x,y,z,w), there exists a single cube
# (really, a hypercube) which is still either active or inactive.

# Each cube only ever considers its neighbors: any of the 80 other cubes
# where any of their coordinates differ by at most 1. For example, given the
# cube at x=1,y=2,z=3,w=4, its neighbors include the cube at x=2,y=2,z=3,w=3,
# the cube at x=0,y=2,z=3,w=4, and so on.

# The initial state of the pocket dimension still consists of a small flat
# region of cubes. Furthermore, the same rules for cycle updating still
# apply: during each cycle, consider the number of active neighbors of each
# cube.

# For example, consider the same initial state as in the example above. Even
# though the pocket dimension is 4-dimensional, this initial state represents
# a small 2-dimensional slice of it. (In particular, this initial state
# defines a 3x3x1x1 region of the 4-dimensional space.)

# Simulating a few cycles from this initial state produces the following
# configurations, where the result of each cycle is shown layer-by-layer at
# each given z and w coordinate:

# Before any cycles:

# z=0, w=0
# .#.
# ..#
# ###


# After 1 cycle:

# z=-1, w=-1
# #..
# ..#
# .#.

# z=0, w=-1
# #..
# ..#
# .#.

# z=1, w=-1
# #..
# ..#
# .#.

# z=-1, w=0
# #..
# ..#
# .#.

# z=0, w=0
# #.#
# .##
# .#.

# z=1, w=0
# #..
# ..#
# .#.

# z=-1, w=1
# #..
# ..#
# .#.

# z=0, w=1
# #..
# ..#
# .#.

# z=1, w=1
# #..
# ..#
# .#.


# After 2 cycles:

# z=-2, w=-2
# .....
# .....
# ..#..
# .....
# .....

# z=-1, w=-2
# .....
# .....
# .....
# .....
# .....

# z=0, w=-2
# ###..
# ##.##
# #...#
# .#..#
# .###.

# z=1, w=-2
# .....
# .....
# .....
# .....
# .....

# z=2, w=-2
# .....
# .....
# ..#..
# .....
# .....

# z=-2, w=-1
# .....
# .....
# .....
# .....
# .....

# z=-1, w=-1
# .....
# .....
# .....
# .....
# .....

# z=0, w=-1
# .....
# .....
# .....
# .....
# .....

# z=1, w=-1
# .....
# .....
# .....
# .....
# .....

# z=2, w=-1
# .....
# .....
# .....
# .....
# .....

# z=-2, w=0
# ###..
# ##.##
# #...#
# .#..#
# .###.

# z=-1, w=0
# .....
# .....
# .....
# .....
# .....

# z=0, w=0
# .....
# .....
# .....
# .....
# .....

# z=1, w=0
# .....
# .....
# .....
# .....
# .....

# z=2, w=0
# ###..
# ##.##
# #...#
# .#..#
# .###.

# z=-2, w=1
# .....
# .....
# .....
# .....
# .....

# z=-1, w=1
# .....
# .....
# .....
# .....
# .....

# z=0, w=1
# .....
# .....
# .....
# .....
# .....

# z=1, w=1
# .....
# .....
# .....
# .....
# .....

# z=2, w=1
# .....
# .....
# .....
# .....
# .....

# z=-2, w=2
# .....
# .....
# ..#..
# .....
# .....

# z=-1, w=2
# .....
# .....
# .....
# .....
# .....

# z=0, w=2
# ###..
# ##.##
# #...#
# .#..#
# .###.

# z=1, w=2
# .....
# .....
# .....
# .....
# .....

# z=2, w=2
# .....
# .....
# ..#..
# .....
# .....

# After the full six-cycle boot process completes, 848 cubes are left in the
# active state.

# Starting with your given initial configuration, simulate six cycles in a
# 4-dimensional space. How many cubes are left in the active state after the
# sixth cycle?

def read_4d_grid(f, iterations) -> Grid:
    (initLayer, xDim, yDim) = read_input(f)
    padd = iterations + 1

    grid = Grid(xDim + 2 * padd, yDim + 2 * padd, 1 + 2 * padd, 1 + 2 * padd)

    for i, line in enumerate(initLayer):
        lineStart = grid.getIndex(padd, i + padd, padd, padd)
        grid.bits[lineStart: lineStart + xDim] = bitarray(line)

    return grid


# with open(os.path.dirname(__file__) + "/../examples/example_17.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_17.txt") as f:
    grid = read_4d_grid(f, iterations)
    for i in range(iterations):
        grid.simulate_cycle()
        print("Cycle " + str(i) + " simulated")

    print("2020 - Day 17 - Part 2")
    print(grid.bits.count())
    # => 2276
    #    ====
