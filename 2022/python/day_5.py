# ---------------------------
# Advent of Code 2022 - Day 5
# Part 1: Supply Stacks
# ---------------------------

# The expedition can depart as soon as the final supplies have been unloaded
# from the ships. Supplies are stored in stacks of marked crates, but because
# the needed supplies are buried under many other crates, the crates need to
# be rearranged.

# The ship has a giant cargo crane capable of moving crates between stacks.
# To ensure none of the crates get crushed or fall over, the crane operator
# will rearrange them in a series of carefully-planned steps. After the
# crates are rearranged, the desired crates will be at the top of each stack.

# The Elves don't want to interrupt the crane operator during this delicate
# procedure, but they forgot to ask her which crate will end up where, and
# they want to be ready to unload them as soon as possible so they can embark.

# They do, however, have a drawing of the starting stacks of crates and the
# rearrangement procedure (your puzzle input). For example:

#     [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3 

# move 1 from 2 to 1
# move 3 from 1 to 3
# move 2 from 2 to 1
# move 1 from 1 to 2

# In this example, there are three stacks of crates. Stack 1 contains two
# crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains
# three crates; from bottom to top, they are crates M, C, and D. Finally,
# stack 3 contains a single crate, P.

# Then, the rearrangement procedure is given. In each step of the procedure,
# a quantity of crates is moved from one stack to a different stack. In the
# first step of the above rearrangement procedure, one crate is moved from
# stack 2 to stack 1, resulting in this configuration:

# [D]        
# [N] [C]    
# [Z] [M] [P]
#  1   2   3

# In the second step, three crates are moved from stack 1 to stack 3. Crates
# are moved one at a time, so the first crate to be moved (D) ends up below
# the second and third crates:

#         [Z]
#         [N]
#     [C] [D]
#     [M] [P]
#  1   2   3

# Then, both crates are moved from stack 2 to stack 1. Again, because crates
# are moved one at a time, crate C ends up below crate M:

#         [Z]
#         [N]
# [M]     [D]
# [C]     [P]
#  1   2   3

# Finally, one crate is moved from stack 1 to stack 2:

#         [Z]
#         [N]
#         [D]
# [C] [M] [P]
#  1   2   3

# The Elves just need to know which crate will end up on top of each stack;
# in this example, the top crates are C in stack 1, M in stack 2, and Z in
# stack 3, so you should combine these together and give the Elves the
# message CMZ.

# After the rearrangement procedure completes, what crate ends up on top of
# each stack?

from __future__ import annotations

import os
import re
from typing import TextIO


def read_data(file: TextIO) -> tuple[list[str], list[str]]:
    containers = []
    movements = []
    found_newline = False
    for line in file.read().split('\n'):
        if not line:
            found_newline = True
            continue
        if found_newline:
            movements.append(line)
        else:
            containers.append(line)
    return containers[:-1], movements


def process_containers(data: list[str]) -> list[list[str]]:
    stacks = [[] for _ in range((len(data[0]) + 3) // 4 + 1)]

    for line in reversed(data):
        chunks = [line[i:i + 4] for i in range(0, len(line), 4)]
        for i, chunk in enumerate(chunks):
            if chunk[1] == ' ':
                continue
            stacks[i].append(chunk[1])

    return stacks


def extract_numbers_from_line(line: str) -> tuple[int, int, int]:
    pattern = r"\b\d+\b"
    numbers = list(map(int, re.findall(pattern, line)))
    return numbers[0], numbers[1], numbers[2]


def prepare_movements(data: list[str]) -> list[tuple[int, int, int]]:
    return [extract_numbers_from_line(line) for line in data]


def process_movements_9000(movements: list[tuple[int, int, int]], stacks: list[list[str]]) -> list[list[str]]:
    for amount, source, destination in movements:
        for _ in range(amount):
            stacks[destination - 1].append(stacks[source - 1].pop())
    return stacks


def get_message(stacks: list[list[str]]) -> str:
    return ''.join([stack[-1] if len(stack) > 0 else '' for stack in stacks])


# with open(os.path.dirname(__file__) + "/../examples/example_5.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_5.txt") as f:
    container_data, movement_data = read_data(f)
    stacks = process_containers(container_data)
    movements = prepare_movements(movement_data)
    reordered_stacks = process_movements_9000(movements, stacks)

    print("2022 - Day 5 - Part 1")
    print(get_message(reordered_stacks))
    # => HNSNMTLHQ
    #    =========

print()


# ---------------------------
# Advent of Code 2022 - Day 5
# Part 2: Supply Stacks
# ---------------------------

# As you watch the crane operator expertly rearrange the crates, you notice
# the process isn't following your prediction.

# Some mud was covering the writing on the side of the crane, and you quickly
# wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

# The CrateMover 9001 is notable for many new and exciting features: air
# conditioning, leather seats, an extra cup holder, and the ability to pick
# up and move multiple crates at once.

# Again considering the example above, the crates begin in the same
# configuration:

#     [D]    
# [N] [C]    
# [Z] [M] [P]
#  1   2   3

# Moving a single crate from stack 2 to stack 1 behaves the same as before:

# [D]        
# [N] [C]    
# [Z] [M] [P]
#  1   2   3

# However, the action of moving three crates from stack 1 to stack 3 means
# that those three moved crates stay in the same order, resulting in this new
# configuration:

#         [D]
#         [N]
#     [C] [Z]
#     [M] [P]
#  1   2   3

# Next, as both crates are moved from stack 2 to stack 1, they retain
# their order as well:

#         [D]
#         [N]
# [C]     [Z]
# [M]     [P]
#  1   2   3

# Finally, a single crate is still moved from stack 1 to stack 2, but now
# it's crate C that gets moved:

#         [D]
#         [N]
#         [Z]
# [M] [C] [P]
#  1   2   3

# In this example, the CrateMover 9001 has put the crates in a totally
# different order: MCD.

# Before the rearrangement process finishes, update your simulation so that
# the Elves know where they should stand to be ready to unload the final
# supplies. After the rearrangement procedure completes, what crate ends up
# on top of each stack?


def process_movements_9001(movements: list[tuple[int, int, int]], stacks: list[list[str]]) -> list[list[str]]:
    for amount, source, destination in movements:
        stacks[destination - 1] += (stacks[source - 1][-amount:])
        stacks[source - 1] = stacks[source - 1][:-amount]
    return stacks


# with open(os.path.dirname(__file__) + "/../examples/example_5.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_5.txt") as f:
    container_data, movement_data = read_data(f)
    stacks = process_containers(container_data)
    movements = prepare_movements(movement_data)
    reordered_stacks = process_movements_9001(movements, stacks)

    print("2022 - Day 5 - Part 2")
    print(get_message(reordered_stacks))
    # => RNLFDJMCT
    #    =========
