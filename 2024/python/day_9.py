from itertools import repeat
from typing import Optional

from solution_base import AocSolution, solution, InputSource

# -------------------
# PART 1: Description
# -------------------

# Another push of the button leaves you in the familiar hallways of some
# friendly amphipods! Good thing you each somehow got your own personal mini
# submarine. The Historians jet away in search of the Chief, mostly by
# driving directly into walls.

# While The Historians quickly figure out how to pilot these things, you
# notice an amphipod in the corner struggling with his computer. He's trying
# to make more contiguous free space by compacting all of the files, but his
# program isn't working; you offer to help.

# He shows you the disk map (your puzzle input) he's already generated. For
# example:

# 2333133121414131402

# The disk map uses a dense format to represent the layout of files and free
# space on the disk. The digits alternate between indicating the length of a
# file and the length of free space.

# So, a disk map like 12345 would represent a one-block file, two blocks of
# free space, a three-block file, four blocks of free space, and then a five-
# block file. A disk map like 90909 would represent three nine-block files in
# a row (with no free space between them).

# Each file on disk also has an ID number based on the order of the files as
# they appear before they are rearranged, starting with ID 0. So, the disk
# map 12345 has three files: a one-block file with ID 0, a three-block file
# with ID 1, and a five-block file with ID 2. Using one character for each
# block where digits are the file ID and . is free space, the disk map 12345
# represents these individual blocks:

# 0..111....22222

# The first example above, 2333133121414131402, represents these individual
# blocks:

# 00...111...2...333.44.5555.6666.777.888899

# The amphipod would like to move file blocks one at a time from the end of
# the disk to the leftmost free space block (until there are no gaps
# remaining between file blocks). For the disk map 12345, the process looks
# like this:

# 0..111....22222
# 02.111....2222.
# 022111....222..
# 0221112...22...
# 02211122..2....
# 022111222......

# The first example requires a few more steps:

# 00...111...2...333.44.5555.6666.777.888899
# 009..111...2...333.44.5555.6666.777.88889.
# 0099.111...2...333.44.5555.6666.777.8888..
# 00998111...2...333.44.5555.6666.777.888...
# 009981118..2...333.44.5555.6666.777.88....
# 0099811188.2...333.44.5555.6666.777.8.....
# 009981118882...333.44.5555.6666.777.......
# 0099811188827..333.44.5555.6666.77........
# 00998111888277.333.44.5555.6666.7.........
# 009981118882777333.44.5555.6666...........
# 009981118882777333644.5555.666............
# 00998111888277733364465555.66.............
# 0099811188827773336446555566..............

# The final step of this file-compacting process is to update the filesystem
# checksum. To calculate the checksum, add up the result of multiplying each
# of these blocks' position with the file ID number it contains. The leftmost
# block is in position 0. If a block contains free space, skip it instead.

# Continuing the first example, the first few blocks' position multiplied by
# its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32,
# and so on. In this example, the checksum is the sum of these, 1928.

# Compact the amphipod's hard drive using the process he requested. What is
# the resulting filesystem checksum? (Be careful copy/pasting the input for
# this puzzle; it is a single, very long line.)

# -------------------
# PART 2: Description
# -------------------

# Upon completion, two things immediately become clear. First, the disk
# definitely has a lot more contiguous free space, just like the amphipod
# hoped. Second, the computer is running much more slowly! Maybe introducing
# all of that file system fragmentation was a bad idea?

# The eager amphipod already has a new plan: rather than move individual
# blocks, he'd like to try compacting the files on his disk by moving whole
# files instead.

# This time, attempt to move whole files to the leftmost span of free space
# blocks that could fit the file. Attempt to move each file exactly once in
# order of decreasing file ID number starting with the file with the highest
# file ID number. If there is no span of free space to the left of a file
# that is large enough to fit the file, the file does not move.

# The first example from above now proceeds differently:

# 00...111...2...333.44.5555.6666.777.888899
# 0099.111...2...333.44.5555.6666.777.8888..
# 0099.1117772...333.44.5555.6666.....8888..
# 0099.111777244.333....5555.6666.....8888..
# 00992111777.44.333....5555.6666.....8888..

# The process of updating the filesystem checksum is the same; now, this
# example's checksum would be 2858.

# Start over, now compacting the amphipod's hard drive using this new method
# instead. What is the resulting filesystem checksum?

DiskMap = list[tuple[bool, int, int]]


def read_disk_map(input_data: InputSource) -> DiskMap:
    disk_map = []
    is_file = True
    block_start_idx = 0
    for c in input_data.read_raw():
        block_length = int(c)
        disk_map.append((is_file, block_start_idx, block_length))
        block_start_idx += block_length
        is_file = not is_file
    return disk_map


def build_blocks(disk_map: DiskMap) -> list[str]:
    blocks: list[str] = []
    is_file = True
    curr_id = 0
    for _, _, block_length in disk_map:
        content = '.'
        if is_file:
            content = str(curr_id)
            curr_id = (curr_id + 1 % 10)
        block = list(repeat(content, block_length))
        blocks.extend(block)
        is_file = not is_file
    return blocks


def find_leftmost_free_space(sorted_blocks: list[str], file_idx: int, file_size: int) -> Optional[int]:
    free_space_idx = None
    free_space_size = 0
    for i in range(file_idx):
        c = sorted_blocks[i]

        if c.isnumeric():
            free_space_idx = None
            free_space_size = 0
        else:
            if not free_space_idx:
                free_space_idx = i
            free_space_size += 1

        if free_space_size >= file_size:
            return free_space_idx

    return None


def move_file(sorted_blocks: list[str], file_idx: int, size: int, free_space_idx: int) -> list[str]:
    for i in range(size):
        sorted_blocks[free_space_idx + i] = sorted_blocks[file_idx + i]
        sorted_blocks[file_idx + i] = '.'
    return sorted_blocks


def sort_blocks(blocks: list[str]) -> list[str]:
    sorted_blocks = blocks.copy()
    i, j = 0, len(blocks) - 1

    while True:
        while sorted_blocks[i] != '.':
            i += 1
        while sorted_blocks[j] == '.':
            j -= 1
        if i >= j:
            return sorted_blocks
        sorted_blocks[i] = blocks[j]
        sorted_blocks[j] = blocks[i]


def calc_checksum(blocks: list[str]) -> int:
    checksum = 0
    for idx, num in enumerate(blocks):
        if num == '.':
            continue
        checksum += idx * int(num)
    return checksum


class Day9(AocSolution):

    @property
    def title(self) -> str:
        return "Disk Fragmenter"

    @property
    def question_part1(self) -> str:
        return "What is the resulting filesystem checksum?"

    @property
    def question_part2(self) -> str:
        return "What is the new resulting filesystem checksum?"

    @solution(6386640365805)
    def solve_part1(self, input_data: InputSource) -> int:
        disk_map = read_disk_map(input_data)
        blocks = build_blocks(disk_map)
        sorted_blocks = sort_blocks(blocks)
        return calc_checksum(sorted_blocks)

    def sort_blocks_keeping_files_intact(self, blocks: list[str], disk_map: DiskMap) -> list[str]:
        sorted_blocks = blocks.copy()
        files_reversed = list(reversed([(idx, size) for is_file, idx, size in disk_map if is_file]))

        progress = self.create_progress(len(files_reversed), 'Sorting Files')

        for file_idx, size in files_reversed:
            progress.update()
            free_space_idx = find_leftmost_free_space(sorted_blocks, file_idx, size)

            if free_space_idx:
                move_file(sorted_blocks, file_idx, size, free_space_idx)

        progress.finish()

        return sorted_blocks

    @solution(6423258376982)
    def solve_part2(self, input_data: InputSource) -> int:
        disk_map = read_disk_map(input_data)
        blocks = build_blocks(disk_map)
        sorted_blocks = self.sort_blocks_keeping_files_intact(blocks, disk_map)
        return calc_checksum(sorted_blocks)


if __name__ == "__main__":
    solution = Day9()

    # Run with example data in debug mode
    # solution.run(part=2, is_example=True, debug=True)

    # Run both parts with real input
    solution.run()
