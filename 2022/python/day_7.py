# -------------------------------
# Advent of Code 2022 - Day 7
# Part 1: No Space Left On Device
# -------------------------------

# You can hear birds chirping and raindrops hitting leaves as the expedition
# proceeds. Occasionally, you can even hear much louder sounds in the
# distance; how big do the animals get out here, anyway?

# The device the Elves gave you has problems with more than just its
# communication system. You try to run a system update:

# $ system-update --please --pretty-please-with-sugar-on-top
# Error: No space left on device
# Perhaps you can delete some files to make space for the update?

# You browse around the filesystem to assess the situation and save the
# resulting terminal output (your puzzle input). For example:

# $ cd /
# $ ls
# dir a
# 14848514 b.txt
# 8504156 c.dat
# dir d
# $ cd a
# $ ls
# dir e
# 29116 f
# 2557 g
# 62596 h.lst
# $ cd e
# $ ls
# 584 i
# $ cd ..
# $ cd ..
# $ cd d
# $ ls
# 4060174 j
# 8033020 d.log
# 5626152 d.ext
# 7214296 k

# The filesystem consists of a tree of files (plain data) and directories
# (which can contain other directories or files). The outermost directory is
# called /. You can navigate around the filesystem, moving into or out of
# directories and listing the contents of the directory you're currently in.

# Within the terminal output, lines that begin with $ are commands you
# executed, very much like some modern computers:

# - cd means change directory. This changes which directory is the current
#   directory, but the specific result depends on the argument:
#     - cd x moves in one level: it looks in the current directory for the
#       directory named x and makes it the current directory.
#     - cd .. moves out one level: it finds the directory that contains
#       the current directory, then makes that directory the current
#       directory.
#     - cd / switches the current directory to the outermost directory, /.

# - ls means list. It prints out all of the files and directories
#   immediately contained by the current directory:
#     - 123 abc means that the current directory contains a file named abc
#       with size 123.
#     - dir xyz means that the current directory contains a directory
#       named xyz.

# Given the commands and output in the example above, you can determine
# that the filesystem looks visually like this:

# - / (dir)
#   - a (dir)
#     - e (dir)
#       - i (file, size=584)
#     - f (file, size=29116)
#     - g (file, size=2557)
#     - h.lst (file, size=62596)
#   - b.txt (file, size=14848514)
#   - c.dat (file, size=8504156)
#   - d (dir)
#     - j (file, size=4060174)
#     - d.log (file, size=8033020)
#     - d.ext (file, size=5626152)
#     - k (file, size=7214296)

# Here, there are four directories: / (the outermost directory), a and d
# (which are in /), and e (which is in a). These directories also contain
# files of various sizes.

# Since the disk is full, your first step should probably be to find
# directories that are good candidates for deletion. To do this, you need to
# determine the total size of each directory. The total size of a directory
# is the sum of the sizes of the files it contains, directly or indirectly.
# (Directories themselves do not count as having any intrinsic size.)

# The total sizes of the directories above can be found as follows:

# - The total size of directory e is 584 because it contains a single file
#   i of size 584 and no other directories.
# - The directory a has total size 94853 because it contains files f (size
#   29116), g (size 2557), and h.lst (size 62596), plus file i indirectly
#   (a contains e which contains i).
# - Directory d has total size 24933642.
# - As the outermost directory, / contains every file. Its total size is
#   48381165, the sum of the size of every file.

# To begin, find all the directories with a total size of at most 100000,
# then calculate the sum of their total sizes. In the example above, these
# directories are a and e; the sum of their total sizes is 95437 (94853 +
# 584). (As in this example, this process can count files more than once!)

# Find all the directories with a total size of at most 100000. What is
# the sum of the total sizes of those directories?

from __future__ import annotations
import os
from typing import TextIO, Dict, List, Set, Tuple
from enum import Enum
from dataclasses import dataclass, field

DEBUG: bool = False
TOTAL_AVAILABLE_SPACE: int = 70000000
NEEDED_UPDATE_SPACE: int = 30000000


def get_absolute_path(parent_path: str, directory_name: str) -> str:
    return f'{parent_path}/{directory_name}' if parent_path != '/' else f'/{directory_name}'


@dataclass
class Directory:
    name: str
    parent_path: str
    sub_directories: Set[Directory] = field(default_factory=set)
    files: List[Tuple[str, int]] = field(default_factory=list)
    size: int = 0
    recompute_size: bool = True

    def __eq__(self, other):
        if isinstance(other, Directory):
            return self.get_path() == other.get_path()
        return False

    def __hash__(self):
        return hash(self.get_path())

    def get_size(self) -> int:
        return self.compute_size() if self.recompute_size else self.size

    def get_path(self) -> str:
        return get_absolute_path(self.parent_path, self.name)

    def add_subdirectory(self, new_dir_name: str) -> Directory:
        new_dir = Directory(new_dir_name, self.get_path())
        self.sub_directories.add(new_dir)
        self.recompute_size = True
        return new_dir

    def add_file(self, file_name: str, file_size: int) -> None:
        self.files.append((file_name, file_size))
        self.recompute_size = True

    def list_files(self) -> List[str]:
        return [f"{name} ({size})" for name, size in self.files]

    def compute_size(self) -> int:
        dir_size = 0
        dir_size += sum([file_size for _, file_size in self.files])
        for sub_dir in self.sub_directories:
            dir_size += sub_dir.get_size()
        self.size = dir_size
        self.recompute_size = False
        return dir_size


class Filesystem:
    directories: Dict[str, Directory] = {
        '/': Directory('', '/')
    }
    current_dir_path: str = '/'
    root_dir_path: str = '/'

    def _get_current_dir(self) -> Directory:
        return self.directories[self.current_dir_path]

    def _get_path_to_sub_directory(self, sub_dir_name: str) -> str:
        return get_absolute_path(self.current_dir_path, sub_dir_name)

    def create_new_sub_directory(self, new_dir_name: str) -> Directory:
        current_dir = self._get_current_dir()
        new_dir = current_dir.add_subdirectory(new_dir_name)
        new_dir_name = self._get_path_to_sub_directory(new_dir_name)
        self.directories.setdefault(new_dir_name, new_dir)
        return new_dir

    def create_new_file(self, file_name: str, file_size: int) -> None:
        current_dir = self._get_current_dir()
        current_dir.add_file(file_name, file_size)

    def change_to_directory(self, target_dir_name: str) -> None:
        if target_dir_name == '/':
            self.current_dir_path = self.root_dir_path
        elif target_dir_name == '..':
            self.change_to_parent_directory()
        else:
            self.change_to_sub_directory(target_dir_name)

    def change_to_sub_directory(self, new_dir_name: str) -> None:
        new_dir_path = self._get_path_to_sub_directory(new_dir_name)
        if new_dir_path not in self.directories:
            self.create_new_sub_directory(new_dir_name)
        self.current_dir_path = new_dir_path

    def change_to_parent_directory(self) -> None:
        self.current_dir_path = self.directories[self.current_dir_path].parent_path

    def get_current_directory_size(self) -> int:
        return self._get_current_dir().get_size()


class Command:
    def handle(self, fs: Filesystem) -> None:
        raise NotImplementedError("Subclasses must implement the handle method.")


class CDCommand(Command):
    directory: str

    def __init__(self, directory: str):
        self.directory = directory

    def __str__(self) -> str:
        return f"CDCommand(dir: {self.directory})"

    def handle(self, fs: Filesystem) -> None:
        prev_dir_path = fs.current_dir_path
        fs.change_to_directory(self.directory)
        if DEBUG:
            print(f"cd {self.directory}: {prev_dir_path} -> {fs.current_dir_path}")


class LSCommand(Command):
    content: list[str]

    def __init__(self, elements: list[str]):
        self.content = elements

    def __str__(self) -> str:
        return f"LSCommand(content: {self.content})"

    def handle(self, fs: Filesystem) -> None:
        names = []
        for element in self.content:
            a, b = element.split(' ')
            if str.isnumeric(a):
                fs.create_new_file(b, int(a))
            else:
                fs.create_new_sub_directory(b)
            names.append(b)
        if DEBUG:
            print(f"ls: {names}")


def parse_command(command_lines: list[str]) -> Command:
    if command_lines[0].startswith('cd'):
        return CDCommand(command_lines[0][3:])
    if command_lines[0].startswith('ls'):
        return LSCommand(command_lines[1:])


def read_commands(file: TextIO) -> list[Command]:
    command_lines = list(map(lambda c: c.strip().split('\n'), file.read().split('$')))[1:]
    return list(map(parse_command, command_lines))


def create_filesystem(commands: list[Command]) -> Filesystem:
    fs = Filesystem()
    for command in commands:
        command.handle(fs)
    return fs


def find_directories_smaller_than(max_size: int, fs: Filesystem) -> List[Directory]:
    smaller_directories = []
    for directory in fs.directories.values():
        if directory.get_size() < max_size:
            smaller_directories.append(directory)
    return smaller_directories


# with open(os.path.dirname(__file__) + "/../examples/example_7.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_7.txt") as f:
    filesystem = create_filesystem(read_commands(f))
    filesystem.get_current_directory_size()
    small_directories = find_directories_smaller_than(100000, filesystem)

    print("2022 - Day 7 - Part 1")
    print(sum(d.get_size() for d in small_directories))
    # => 1783610
    #    =======

print()

# -------------------------------
# Advent of Code 2022 - Day 7
# Part 2: No Space Left On Device
# -------------------------------

# Now, you're ready to choose a directory to delete.
#
# The total disk space available to the filesystem is 70000000. To run the
# update, you need unused space of at least 30000000. You need to find a
# directory you can delete that will free up enough space to run the update.
#
# In the example above, the total size of the outermost directory (and thus
# the total amount of used space) is 48381165; this means that the size of
# the unused space must currently be 21618835, which isn't quite the 30000000
# required by the update. Therefore, the update still requires a directory
# with total size of at least 8381165 to be deleted before it can run.
#
# To achieve this, you have the following options:
#
# Delete directory e, which would increase unused space by 584.
# Delete directory a, which would increase unused space by 94853.
# Delete directory d, which would increase unused space by 24933642.
# Delete directory /, which would increase unused space by 48381165.

# Directories e and a are both too small; deleting them would not free up
# enough space. However, directories d and / are both big enough! Between
# these, choose the smallest: d, increasing unused space by 24933642.
#
# Find the smallest directory that, if deleted, would free up enough space on
# the filesystem to run the update. What is the total size of that directory?


def find_big_enough_directories(needed_size: int, fs: Filesystem) -> List[Directory]:
    possible_directories = []
    for directory in fs.directories.values():
        if directory.get_size() >= needed_size:
            possible_directories.append(directory)
    return possible_directories


def find_smallest_directory(directories: List[Directory]) -> Directory:
    directories.sort(key=lambda directory: directory.size)
    return directories[0]


def calc_needed_space(fs: Filesystem) -> int:
    root_dir_size = fs.directories[filesystem.root_dir_path].get_size()
    unused_space = TOTAL_AVAILABLE_SPACE - root_dir_size
    return abs(NEEDED_UPDATE_SPACE - unused_space)


# with open(os.path.dirname(__file__) + "/../examples/example_7.txt") as f:
with open(os.path.dirname(__file__) + "/../inputs/input_7.txt") as f:
    # filesystem = create_filesystem(read_commands(f))
    big_directories = find_big_enough_directories(calc_needed_space(filesystem), filesystem)
    size = find_smallest_directory(big_directories).get_size()
    print("2022 - Day 7 - Part 2")
    print(size)
    # => 4370655
    #    =======
