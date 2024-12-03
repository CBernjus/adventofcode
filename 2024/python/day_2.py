DAY = 2
# ---------------------------
# Advent of Code 2024 - Day 2
# Part 1: Red-Nosed Reports
# ---------------------------

# Fortunately, the first location The Historians want to search isn't a long
# walk from the Chief Historian's office.

# While the Red-Nosed Reindeer nuclear fusion/fission plant appears to
# contain no sign of the Chief Historian, the engineers there run up to you
# as soon as they see you. Apparently, they still talk about the time Rudolph
# was saved through molecular synthesis from a single electron.

# They're quick to add that - since you're already here - they'd really
# appreciate your help analyzing some unusual data from the Red-Nosed
# reactor. You turn to check if The Historians are waiting for you, but they
# seem to have already divided into groups that are currently searching every
# corner of the facility. You offer to help with the unusual data.

# The unusual data (your puzzle input) consists of many reports, one report
# per line. Each report is a list of numbers called levels that are separated
# by spaces. For example:

# 7 6 4 2 1
# 1 2 7 8 9
# 9 7 6 2 1
# 1 3 2 4 5
# 8 6 4 4 1
# 1 3 6 7 9

# This example data contains six reports each containing five levels.

# The engineers are trying to figure out which reports are safe. The Red-
# Nosed reactor safety systems can only tolerate levels that are either
# gradually increasing or gradually decreasing. So, a report only counts as
# safe if both of the following are true:

# - The levels are either all increasing or all decreasing.
# - Any two adjacent levels differ by at least one and at most three.

# In the example above, the reports can be found safe or unsafe by checking
# those rules:

# - 7 6 4 2 1: Safe because the levels are all decreasing by 1 or 2.
# - 1 2 7 8 9: Unsafe because 2 7 is an increase of 5.
# - 9 7 6 2 1: Unsafe because 6 2 is a decrease of 4.
# - 1 3 2 4 5: Unsafe because 1 3 is increasing but 3 2 is decreasing.
# - 8 6 4 4 1: Unsafe because 4 4 is neither an increase or a decrease.
# - 1 3 6 7 9: Safe because the levels are all increasing by 1, 2, or 3.

# So, in this example, 2 reports are safe.

# Analyze the unusual data from the engineers. How many reports are safe?

import os


def get_levels(line: str) -> list[int]:
    return list(map(int, line.split()))


def safe_distance(x: int, y: int) -> bool:
    distance = abs(x - y)
    return 1 <= distance <= 3


def is_safe(report: list[int]) -> bool:
    if len(report) < 2:
        return True

    is_inc = report[1] > report[0]
    is_dec = report[1] < report[0]

    if is_inc and is_dec:
        raise ValueError("The values cannot be increasing and decreasing at the same time.")

    for x, y in zip(report[0:-1:1], report[1::1]):
        if is_inc and x >= y:
            return False
        if is_dec and x <= y:
            return False
        if not safe_distance(x, y):
            return False

    return True


# with open(os.path.dirname(__file__) + f"/../examples/example_{DAY}.txt") as f:
with open(os.path.dirname(__file__) + f"/../inputs/input_{DAY}.txt") as f:
    reports = list(get_levels(line) for line in f.readlines())
    safe_reports = list(filter(is_safe, reports))

    print(f"2024 - Day {DAY} - Part 1")
    print("How many reports are safe?")
    print(len(safe_reports))
    # => 371
    #    =======

print()


# ---------------------------
# Advent of Code 2024 - Day 2
# Part 2: Red-Nosed Reports
# ---------------------------

# The engineers are surprised by the low number of safe reports until they
# realize they forgot to tell you about the Problem Dampener.

# The Problem Dampener is a reactor-mounted module that lets the reactor
# safety systems tolerate a single bad level in what would otherwise be a
# safe report. It's like the bad level never happened!

# Now, the same rules apply as before, except if removing a single level from
# an unsafe report would make it safe, the report instead counts as safe.

# More of the above example's reports are now safe:

# - 7 6 4 2 1: Safe without removing any level.
# - 1 2 7 8 9: Unsafe regardless of which level is removed.
# - 9 7 6 2 1: Unsafe regardless of which level is removed.
# - 1 3 2 4 5: Safe by removing the second level, 3.
# - 8 6 4 4 1: Safe by removing the third level, 4.
# - 1 3 6 7 9: Safe without removing any level.

# Thanks to the Problem Dampener, 4 reports are actually safe!

# Update your analysis by handling situations where the Problem Dampener can
# remove a single level from unsafe reports. How many reports are now safe?


def get_variations(report: list[int], gap_size: int) -> list[list[int]]:
    """return all variations where the number of dampening_level adjacent items are missing.
        for example: ([1, 2, 3], 1) -> [[2, 3], [1, 3], [1, 2]]
        for example: ([1, 2, 3], 2) -> [[3], [1]]
    """
    if gap_size < 0 or gap_size >= len(report):
        raise ValueError("The gap size must be between 0 and the length of the report.")

    variations = []
    for i in range(len(report)):
        if i + gap_size > len(report):
            break
        variations.append(report[:i] + report[i + gap_size:])
    return variations


def can_be_dampened(report: list[int], level: int = 1) -> bool:
    return any(is_safe(variations) for variations in get_variations(report, level))


def is_dampened_safe(report: list[int]) -> bool:
    return is_safe(report) or can_be_dampened(report)


# with open(os.path.dirname(__file__) + f"/../examples/example_{DAY}.txt") as f:
with open(os.path.dirname(__file__) + f"/../inputs/input_{DAY}.txt") as f:
    reports = list(get_levels(line) for line in f.readlines())
    safe_reports = list(filter(is_dampened_safe, reports))

    print(f"2024 - Day {DAY} - Part 2")
    print("How many reports are now safe?")
    print(len(safe_reports))
    # => 426
    #    ==========
