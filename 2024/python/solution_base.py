# aoc/solution_base.py
import logging
import os
import shutil
import sys
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Any, Optional, List, Iterator, TypeVar

from colorama import Style, init


class CustomFormatter(logging.Formatter):
    green = "\x1b[32;20m"
    grey = "\x1b[38;20m"
    yellow = "\x1b[33;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(levelname)s (%(filename)s:%(lineno)d) - %(message)s"

    FORMATS = {
        logging.DEBUG: Style.DIM + grey + format + reset + Style.RESET_ALL,
        logging.INFO: grey + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

    @staticmethod
    def get_console_handler() -> logging.StreamHandler:
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(CustomFormatter())
        return ch


def bold(s: str) -> str:
    return f"{Style.BRIGHT}{s}{Style.RESET_ALL}"


class ProgressStatus:
    def __init__(self, total: int, desc: str = "Progress", show_count: bool = True, verbose: bool = True):
        """
        Initialize progress status bar

        Args:
            total: Total number of items
            desc: Description to show before the progress
            show_count: Whether to show count (x/total) in addition to percentage
        """
        self.total = total
        self.current = 0
        self.desc = desc
        self.show_count = show_count
        self.verbose = verbose
        self.terminal_width = shutil.get_terminal_size().columns
        self._last_len = 0
        self.extras = {}

    def update(self, step: int = 1, **kwargs) -> None:
        """
        Update progress by step amount and optionally update extra values

        Args:
            step: Amount to increment progress
            **kwargs: Extra key-value pairs to display (e.g., loops_found=5)
        """
        self.current += step
        self.extras.update(kwargs)
        if self.verbose:
            self._print_progress()

    def _print_progress(self) -> None:
        percentage = (self.current / self.total) * 100

        # Build progress message
        msg_parts = [f"{self.desc}:"]

        if self.show_count:
            msg_parts.append(f"{self.current}/{self.total}")

        msg_parts.append(f"({percentage:.1f}%)")

        # Add any extra information
        for key, value in self.extras.items():
            msg_parts.append(f"| {key}: {value}")

        message = " ".join(msg_parts)

        # Clear previous line and print new progress
        print(f"\r{message.ljust(self.terminal_width)}", end="", file=sys.stdout)
        sys.stdout.flush()

    def finish(self) -> None:
        """Complete the progress and move to next line"""
        if self.verbose:
            print(file=sys.stdout)
            sys.stdout.flush()


T = TypeVar('T')


class ResultStatus(Enum):
    CORRECT = "√"
    INCORRECT = "x"
    UNKNOWN = "!"


def status_color(s: str, status: ResultStatus, is_example: bool = False) -> str:
    color = CustomFormatter.yellow
    if not is_example:
        if status == ResultStatus.CORRECT:
            color = CustomFormatter.green
        if status == ResultStatus.INCORRECT:
            color = CustomFormatter.red
    return color + s + CustomFormatter.reset


@dataclass
class Result:
    value: Any
    execution_time: float
    status: ResultStatus = ResultStatus.UNKNOWN


class InputSource:
    def __init__(self, day: int, part: int, is_example: bool, example_suffix: str = None):
        self.day = day
        self.part = part
        self.is_example = is_example
        self.example_suffix = example_suffix
        init()

    def _get_input_path(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        file_prefix = "example" if self.is_example else "input"
        folder = file_prefix + 's'

        # Try part-specific input first
        specific_path = os.path.join(base_dir, folder, f"{file_prefix}_{self.day}_{self.part}.txt")
        if os.path.exists(specific_path):
            return specific_path

        # Try example input with suffix next
        if self.is_example and self.example_suffix:
            suffix_specific_path = os.path.join(base_dir, folder,
                                                f"{file_prefix}_{self.day}_{self.part}_{self.example_suffix}.txt")
            if os.path.exists(suffix_specific_path):
                return suffix_specific_path

            suffix_path = os.path.join(base_dir, folder, f"{file_prefix}_{self.day}_{self.example_suffix}.txt")
            if os.path.exists(suffix_path):
                return suffix_path

        # Fall back to common input
        return os.path.join(base_dir, folder, f"{file_prefix}_{self.day}.txt")

    def read_raw(self) -> str:
        """Read the raw input file"""
        with open(self._get_input_path()) as f:
            return f.read().strip()

    def read_lines(self, strip: bool = True) -> List[str]:
        """Read input as list of lines"""
        with open(self._get_input_path()) as f:
            if strip:
                return [line.strip() for line in f.readlines()]
            return [line.rstrip('\n') for line in f.readlines()]

    def read_lists_of_integers(self, seperator: str = None) -> List[List[int]]:
        """Read input as list of lists of integers, split by seperator (default: None -> any whitespace)"""
        string_lists = [line.strip().split(seperator) for line in self.read_lines()]
        return [[int(num.strip()) for num in l] for l in string_lists]

    def read_sections(self) -> List[str]:
        """Read input split by double newlines"""
        return self.read_raw().split('\n\n')

    def read_integers(self) -> List[int]:
        """Read input as list of integers"""
        return [int(line) for line in self.read_lines()]

    def read_digit_grid(self) -> List[List[int]]:
        """Read input as 2D grid of single digits"""
        return [[int(d) for d in line] for line in self.read_lines()]

    def read_char_grid(self) -> List[List[str]]:
        """Read input as 2D character grid"""
        return [list(line) for line in self.read_lines()]

    def read_sections_of_lines(self) -> List[List[str]]:
        """Read input as sections of lines, split by double newlines"""
        return [section.split('\n') for section in self.read_sections()]

    def read_as_iterator(self) -> Iterator[str]:
        """Read input as an iterator of lines (memory efficient for large inputs)"""
        with open(self._get_input_path()) as f:
            for line in f:
                yield line.strip()


def solution(expected_result: Any = None):
    """Decorator to annotate solutions with expected results"""

    def decorator(func):
        @wraps(func)
        def wrapper(self, input_source: InputSource, *args, **kwargs):
            result = func(self, input_source, *args, **kwargs)
            if expected_result is not None:
                if result == expected_result:
                    return Result(result, 0, ResultStatus.CORRECT)
                return Result(result, 0, ResultStatus.INCORRECT)
            return Result(result, 0, ResultStatus.UNKNOWN)

        return wrapper

    return decorator


def _print_verbose(message: str, verbose: bool) -> None:
    if verbose:
        print(message)


class AocSolution(ABC):
    @property
    def day(self) -> int:
        """Extract day number from class name (Day1 -> 1)"""
        return int(self.__class__.__name__.removeprefix('Day'))

    @property
    @abstractmethod
    def title(self) -> str:
        """Return the puzzle title"""
        pass

    @property
    @abstractmethod
    def question_part1(self) -> str:
        pass

    @abstractmethod
    def question_part2(self) -> str:
        pass

    def __init__(self):
        self.logger = logging.getLogger(f"AOC_Day_{self.day}")
        self.logger.addHandler(CustomFormatter.get_console_handler())
        self.progress_verbose = True

    @staticmethod
    def _time_execution(func, *args, **kwargs) -> Result:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        if not isinstance(result, Result):
            result = Result(result, 0, ResultStatus.UNKNOWN)
        end_time = time.perf_counter()
        result.execution_time = end_time - start_time
        return result

    def execute_part(self, part: int, is_example: bool, example_suffix: str = None, verbose: bool = True,
                     log_prefix: str = '') -> None:
        input_source = InputSource(self.day, part, is_example, example_suffix)
        solver = self.solve_part1 if part == 1 else self.solve_part2
        result = self._time_execution(solver, input_source)
        time_str = f"{result.execution_time * 1000:.2f} ms" if result.execution_time < 1 else f"{result.execution_time:.2f} s"
        _print_verbose(log_prefix +
                       status_color(f"[{'-' if is_example else result.status.value}] {bold(result.value)} ({time_str})",
                                    result.status, is_example),
                       verbose)

    def _set_logging_level(self, debug: bool, verbose: bool) -> None:
        if debug:
            self.logger.setLevel(logging.DEBUG)
        elif verbose:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.WARNING)

    def create_progress(self, total: int, desc: str = "Progress", show_count: bool = True) -> ProgressStatus:
        """
        Create a new progress status tracker

        Args:
            total: Total number of items
            desc: Description to show before the progress
            show_count: Whether to show count in addition to percentage

        Returns:
            ProgressStatus object for updating progress
        """
        return ProgressStatus(total, desc, show_count, self.progress_verbose)

    def run(self, part: Optional[int] = None, is_example: bool = False, example_suffix: str = None, debug: bool = False,
            verbose: bool = True) -> None:
        self._set_logging_level(debug, verbose)
        self.progress_verbose = verbose
        _print_verbose(bold(f"\n2024 - Day {self.day} - {self.title}"), verbose)

        if part in {1, None}:
            _print_verbose(f"{bold('Part 1:')} {self.question_part1}", verbose)
            self.execute_part(1, is_example, example_suffix, verbose)

        if part in {2, None}:
            _print_verbose(f"{bold('Part 2:')} {self.question_part2}", verbose)
            self.execute_part(2, is_example, example_suffix, verbose)

    @abstractmethod
    def solve_part1(self, input_source: InputSource) -> Any:
        pass

    @abstractmethod
    def solve_part2(self, input_source: InputSource) -> Any:
        pass
