# aoc/solution_base.py
import logging
import os
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import wraps
from typing import Any, Optional, List, Iterator, TypeVar

T = TypeVar('T')


class ResultStatus(Enum):
    CORRECT = "✅"
    INCORRECT = "❌"
    UNKNOWN = "⚠️"


@dataclass
class Result:
    value: Any
    execution_time: float
    status: ResultStatus = ResultStatus.UNKNOWN


class InputSource:
    def __init__(self, day: int, part: int, is_example: bool):
        self.day = day
        self.part = part
        self.is_example = is_example

    def _get_input_path(self) -> str:
        base_dir = os.path.dirname(os.path.dirname(__file__))
        folder = "examples" if self.is_example else "inputs"

        # Try part-specific input first
        specific_path = os.path.join(base_dir, folder, f"{folder[:-1]}_{self.day}_{self.part}.txt")
        if os.path.exists(specific_path):
            return specific_path

        # Fall back to common input
        return os.path.join(base_dir, folder, f"{folder[:-1]}_{self.day}.txt")

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

    def read_sections(self) -> List[str]:
        """Read input split by double newlines"""
        return self.read_raw().split('\n\n')

    def read_integers(self) -> List[int]:
        """Read input as list of integers"""
        return [int(line) for line in self.read_lines()]

    def read_digits(self) -> List[List[int]]:
        """Read input as 2D grid of single digits"""
        return [[int(d) for d in line] for line in self.read_lines()]

    def read_grid(self) -> List[List[str]]:
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

    def parse_lines_as(self, parser: callable[[str], T]) -> List[T]:
        """Parse lines using the provided parser function"""
        return [parser(line) for line in self.read_lines()]


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


class AocSolution(ABC):
    @property
    def day(self) -> int:
        """Extract day number from filename (day_1.py -> 1)"""
        return int(os.path.basename(self.__module__).split('_')[1].split('.')[0])

    @property
    @abstractmethod
    def title(self) -> str:
        """Return the puzzle title"""
        pass

    def __init__(self):
        self.logger = logging.getLogger(f"AOC_Day_{self.day}")

    def _time_execution(self, func, *args, **kwargs) -> Result:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        if not isinstance(result, Result):
            result = Result(result, 0, ResultStatus.UNKNOWN)
        end_time = time.perf_counter()
        result.execution_time = end_time - start_time
        return result

    def run(self, part: Optional[int] = None, is_example: bool = False, debug: bool = False) -> None:
        logging.basicConfig(
            level=logging.DEBUG if debug else logging.INFO,
            format='%(levelname)s - %(message)s'
        )

        print(f"\n2024 - Day {self.day} - {self.title}")

        if part in {1, None}:
            input_source = InputSource(self.day, 1, is_example)
            result = self._time_execution(self.solve_part1, input_source)
            time_str = f"{result.execution_time * 1000:.2f}ms" if result.execution_time < 1 else f"{result.execution_time:.2f}s"
            print(f"Part 1: {result.status.value} {result.value} in {time_str}")

        if part in {2, None}:
            input_source = InputSource(self.day, 2, is_example)
            result = self._time_execution(self.solve_part2, input_source)
            time_str = f"{result.execution_time * 1000:.2f}ms" if result.execution_time < 1 else f"{result.execution_time:.2f}s"
            print(f"Part 2: {result.status.value} {result.value} in {time_str}")

    @abstractmethod
    def solve_part1(self, input_source: InputSource) -> Any:
        pass

    @abstractmethod
    def solve_part2(self, input_source: InputSource) -> Any:
        pass
