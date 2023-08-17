# ---------------------------
# Advent of Code 2022 - Day 8
# Part 1: Treetop Tree House
# ---------------------------

# The expedition comes across a peculiar patch of tall trees all planted
# carefully in a grid. The Elves explain that a previous expedition planted
# these trees as a reforestation effort. Now, they're curious if this would
# be a good location for a tree house.

# First, determine whether there is enough tree cover here to keep a tree
# house hidden. To do this, you need to count the number of trees that are
# visible from outside the grid when looking directly along a row or column.

# The Elves have already launched a quadcopter to generate a map with the
# height of each tree (your puzzle input). For example:

# 30373
# 25512
# 65332
# 33549
# 35390

# Each tree is represented as a single digit whose value is its height, where
# 0 is the shortest and 9 is the tallest.

# A tree is visible if all the other trees between it and an edge of the
# grid are shorter than it. Only consider trees in the same row or column;
# that is, only look up, down, left, or right from any given tree.

# All the trees around the edge of the grid are visible - since they are
# already on the edge, there are no trees to block the view. In this example,
# that only leaves the interior nine trees to consider:

#  - The top-left 5 is visible from the left and top. (It isn't visible
#    from the right or bottom since other trees of height 5 are in the way.)
#  - The top-middle 5 is visible from the top and right.
#  - The top-right 1 is not visible from any direction; for it to be visible,
#    there would need to only be trees of height 0 between it and an edge.
#  - The left-middle 5 is visible, but only from the right.
#  - The center 3 is not visible from any direction; for it to be visible,
#    there would need to be only trees of at most height 2 between it and an
#    edge.
#  - The right-middle 3 is visible from the right.
#  - In the bottom row, the middle 5 is visible, but the 3 and 4 are not.

# With 16 trees visible on the edge and another 5 visible in the interior, a
# total of 21 trees are visible in this arrangement.

# Consider your map; how many trees are visible from outside the grid?

from __future__ import annotations
import os
import numpy as np
import numpy.typing as npt
from typing import TextIO, Dict, List, Tuple


def parse_input(file: TextIO) -> npt.NDArray[int]:
    lines = file.readlines()
    return np.array([list(map(int, list(line.strip()))) for line in lines])


def generate_bitmask_for_list(nums: npt.NDArray[int]) -> npt.NDArray[int]:
    """
    Generate a bitmask for a given 1D list of numbers indicating visibility from the start to the end.
    The bitmask starts and ends with ones, and has zeros for numbers that aren't visible from matrix borders.
    """
    if nums.ndim != 1:
        raise ValueError("Expected a 1D array.")

    length = len(nums)
    bitmask = np.ones(length, dtype=int)
    max_val = nums[0]

    for i in range(1, length - 1):
        if nums[i] <= max_val:
            bitmask[i] = 0
        else:
            max_val = nums[i]

    return bitmask


def generate_bitmask(matrix: npt.NDArray[int]) -> npt.NDArray[int]:
    """
    Generate a bitmask matrix indicating visibility from matrix borders.
    """
    if matrix.ndim != 2:
        raise ValueError("Input matrix should be 2D.")

    rows, cols = matrix.shape
    bitmask = np.zeros((rows, cols), dtype=int)  # start with all ones and then use AND operation

    for r in range(rows):
        bitmask[r, :] |= generate_bitmask_for_list(matrix[r, :])
        bitmask[r, :] |= generate_bitmask_for_list(matrix[r, ::-1])[::-1]  # Compute for reversed and then reverse result

    for c in range(cols):
        bitmask[:, c] |= generate_bitmask_for_list(matrix[:, c])
        bitmask[:, c] |= generate_bitmask_for_list(matrix[::-1, c])[::-1]  # Compute for reversed and then reverse result

    return bitmask


# with open(os.path.dirname(__file__) + "/../examples/example_8.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_8.txt") as f:
    data = parse_input(f)
    visibility_bitmask = generate_bitmask(data)

    print("2022 - Day 8 - Part 1")
    print("How many trees are visible from outside the grid?")
    print(int(np.sum(visibility_bitmask)))
    # => 1835
    #    ====

print()

# ---------------------------
# Advent of Code 2022 - Day 8
# Part 2: Treetop Tree House
# ---------------------------

# Content with the amount of tree cover available, the Elves just need to
# know the best spot to build their tree house: they would like to be able to
# see a lot of trees.

# To measure the viewing distance from a given tree, look up, down, left, and
# right from that tree; stop if you reach an edge or at the first tree that is
# the same height or taller than the tree under consideration. (If a tree is
# right on the edge, at least one of its viewing distances will be zero.)

# The Elves don't care about distant trees taller than those found by the
# rules above; the proposed tree house has large eaves to keep it dry, so
# they wouldn't be able to see higher than the tree house anyway.

# In the example above, consider the middle 5 in the second row:

# 30373
# 25512
# 65332
# 33549
# 35390

# - Looking up, its view is not blocked; it can see 1 tree (of height 3).
# - Looking left, its view is blocked immediately; it can see only 1 tree
#   (of height 5, right next to it).
# - Looking right, its view is not blocked; it can see 2 trees.
# - Looking down, its view is blocked eventually; it can see 2 trees (one
#   of height 3, then the tree of height 5 that blocks its view).

# A tree's scenic score is found by multiplying together its viewing
# distance in each of the four directions. For this tree, this is 4
# (found by multiplying 1 * 1 * 2 * 2).

# However, you can do even better: consider the tree of height 5 in the
# middle of the fourth row:

# 30373
# 25512
# 65332
# 33549
# 35390

# - Looking up, its view is blocked at 2 trees (by another tree with
#   a height of 5).
# - Looking left, its view is not blocked; it can see 2 trees.
# - Looking down, its view is also not blocked; it can see 1 tree.
# - Looking right, its view is blocked at 2 trees (by a massive tree
#   of height 9).

# This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal
# spot for the tree house.

# Consider each tree on your map. What is the highest scenic score
# possible for any tree?


def get_viewing_distance(trees: npt.NDArray[int], height: int) -> int:
    counter = 0

    for tree in trees:
        counter += 1
        if tree >= height:
            return counter

    return counter


def calc_score(matrix: npt.NDArray[int], row: int, col: int) -> int:
    spot = matrix[row, col]
    score = 1

    # check left, right, above, and below
    score *= get_viewing_distance(matrix[row, :col][::-1], spot)
    score *= get_viewing_distance(matrix[row, col+1:], spot)
    score *= get_viewing_distance(matrix[:row, col][::-1], spot)
    score *= get_viewing_distance(matrix[row+1:, col], spot)

    return score


def generate_scenic_scores(matrix: npt.NDArray[int]) -> npt.NDArray[int]:
    scores = np.zeros_like(matrix)

    rows, cols = matrix.shape
    for row in range(rows):
        for col in range(cols):
            scores[row, col] = calc_score(matrix, row, col)

    return scores


# with open(os.path.dirname(__file__) + "/../examples/example_8.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_8.txt") as f:

    data = parse_input(f)
    scenic_scores = generate_scenic_scores(data)

    print("2022 - Day 8 - Part 2")
    print("hat is the highest scenic score possible for any tree?")
    print(np.max(scenic_scores))
    # => 263670
    #    ======
