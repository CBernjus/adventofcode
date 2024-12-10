import argparse
import importlib
import logging
import os
import sys
import time
import traceback
import tracemalloc
from typing import List, Type, Optional, Set, Tuple, Dict

from solution_base import (AocSolution, bold, CustomFormatter,
                           InputSource, ProgressStatus)


class BenchmarkResult:
    def __init__(self, times: List[float], memory: List[float], error: Optional[str] = None):
        self.times = times
        self.memory = memory
        self.error = error

    @property
    def avg_time(self) -> float:
        return sum(self.times) / len(self.times) if self.times else 0

    @property
    def min_time(self) -> float:
        return min(self.times) if self.times else 0

    @property
    def avg_memory(self) -> float:
        return sum(self.memory) / len(self.memory) if self.memory else 0

    @property
    def peak_memory(self) -> float:
        return max(self.memory) if self.memory else 0


class AocRunner:
    SLOW_THRESHOLD = 10.0  # seconds
    MIN_RUNS_FOR_SLOW = 2  # minimum runs for slow solutions

    def __init__(self):
        self.logger = logging.getLogger("AOC_Runner")
        self.logger.addHandler(CustomFormatter.get_console_handler())
        self.logger.setLevel(logging.INFO)

    def discover_solutions(self) -> List[Type[AocSolution]]:
        """Discover all day solution classes in the current directory"""
        solutions = []
        current_dir = os.path.dirname(os.path.abspath(__file__))

        for filename in os.listdir(current_dir):
            if filename.startswith("day_") and filename.endswith(".py"):
                try:
                    day_number = int(filename.removeprefix("day_").removesuffix(".py"))
                    module_name = filename[:-3]
                    module = importlib.import_module(module_name)

                    for item_name in dir(module):
                        if item_name.startswith("Day"):
                            day_class = getattr(module, item_name)
                            if (issubclass(day_class, AocSolution) and
                                    day_class != AocSolution):
                                solutions.append((day_number, day_class))
                                break
                except Exception as e:
                    self.logger.error(f"Error loading {filename}: {e}")

        return [cls for _, cls in sorted(solutions, key=lambda x: x[0])]

    def run_single_benchmark(self, solution: AocSolution, part: int) -> Tuple[float, float]:
        """Run a single benchmark iteration and return (time, memory)"""
        tracemalloc.start()
        start = time.perf_counter()

        try:
            if part == 1:
                solution.solve_part1(InputSource(solution.day, 1, False))
            else:
                solution.solve_part2(InputSource(solution.day, 2, False))

            execution_time = time.perf_counter() - start
            _, peak = tracemalloc.get_traced_memory()
            return execution_time, peak / 1024 / 1024  # Convert to MB
        finally:
            tracemalloc.stop()

    def benchmark_solution(self, solution: AocSolution, max_runs: int = 10) -> Dict[str, BenchmarkResult]:
        """Benchmark a solution with adaptive runs for slow solutions"""
        results = {
            "part1": BenchmarkResult([], []),
            "part2": BenchmarkResult([], [])
        }

        solution.progress_verbose = False
        progress_desc = f"Benchmark Day {solution.day:02d}"

        for part in [1, 2]:
            # First create a progress bar with just one step to show the first run
            progress = ProgressStatus(1,
                                      desc=progress_desc,
                                      show_count=False)
            try:
                progress.update(0, part=part, current_run=0)
                # First run to check execution time
                execution_time, memory = self.run_single_benchmark(solution, part)
                results[f"part{part}"].times.append(execution_time)
                results[f"part{part}"].memory.append(memory)

                # Determine number of runs based on execution time
                remaining_runs = (AocRunner.MIN_RUNS_FOR_SLOW if execution_time > AocRunner.SLOW_THRESHOLD
                                  else max_runs - 1)

                if execution_time > AocRunner.SLOW_THRESHOLD:
                    # Update progress for slow solution
                    progress = ProgressStatus(
                        AocRunner.MIN_RUNS_FOR_SLOW,
                        desc=progress_desc,
                        show_count=False
                    )
                    progress.update(1, part=part, current_run=1,
                                    status=f"Slow solution ({execution_time:.1f}s), reducing to {remaining_runs + 1} runs")
                else:
                    # Update progress for normal solution
                    progress = ProgressStatus(
                        max_runs,
                        desc=progress_desc,
                        show_count=False
                    )
                    progress.update(1, part=part, current_run=1)

                # Remaining runs
                for run in range(remaining_runs):
                    execution_time, memory = self.run_single_benchmark(solution, part)
                    results[f"part{part}"].times.append(execution_time)
                    results[f"part{part}"].memory.append(memory)
                    progress.update(1, current_run=run + 2)

            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])
                error_line = tb[-1].lineno
                error_type = type(e).__name__
                error_msg = f"{error_type} at line {error_line}: {str(e)}"
                results[f"part{part}"].error = error_msg
            finally:
                progress.finish()
                # Clear the progress line
                sys.stdout.write("\033[F\033[K")

        return results

    def get_part_color(self, part_results: BenchmarkResult) -> str:
        """Determine color based on performance"""
        if part_results.error:
            return CustomFormatter.red
        if not part_results.times:
            return CustomFormatter.red
        if part_results.avg_time > self.SLOW_THRESHOLD:
            return CustomFormatter.red
        if part_results.avg_time > 0.1:
            return CustomFormatter.yellow
        return CustomFormatter.green

    def print_benchmark_results(self, solution: AocSolution, results: Dict[str, BenchmarkResult]):
        """Print benchmark results with colored output"""
        print(f"{bold(f'Day {solution.day:02d}')} - {solution.title}")

        for part in [1, 2]:
            part_results = results[f"part{part}"]
            part_color = self.get_part_color(part_results)

            print(f"  {part_color}Part {part}:{CustomFormatter.reset}")

            if part_results.error:
                print(f"    {CustomFormatter.red}Error: {part_results.error}{CustomFormatter.reset}")
            else:
                time_str = f"{part_results.avg_time * 1000:6.1f}ms" if part_results.avg_time < 1 else f"{part_results.avg_time:6.1f}s"
                min_time_str = f"{part_results.min_time * 1000:6.1f}ms" if part_results.min_time < 1 else f"{part_results.min_time:6.1f}s"

                print(f"    Time: {part_color}{time_str}{CustomFormatter.reset} " +
                      f"(min: {min_time_str})")
                print(f"    Mem:  {part_color}{part_results.peak_memory:6.1f}MB{CustomFormatter.reset} " +
                      f"(avg: {part_results.avg_memory:6.1f}MB)")

    def run_solution(self, solution: AocSolution, verbose: bool = True) -> None:
        """Run a single solution with error handling"""
        print(f"\n{bold(f'Day {solution.day:02d} - {solution.title}')}")
        for part in [1, 2]:
            try:
                solution.execute_part(part, False, True, bold(f'Part {part}: '))
            except Exception as e:
                tb = traceback.extract_tb(sys.exc_info()[2])
                error_line = tb[-1].lineno
                error_type = type(e).__name__
                print(f"  {CustomFormatter.red}Part {part}: {error_type} at line {error_line}{CustomFormatter.reset}")
                if verbose:
                    print(f"  {CustomFormatter.red}{str(e)}{CustomFormatter.reset}")

    def run(self, days: Optional[Set[int]] = None, skip_days: Optional[Set[int]] = None,
            benchmark: bool = False, benchmark_runs: int = 10, verbose: bool = True) -> None:
        """Run solutions with optional benchmarking"""
        solutions = self.discover_solutions()

        if not solutions:
            self.logger.error("No solutions found!")
            return

        # Filter solutions based on days and skip_days
        if days is not None:
            solutions = [s for s in solutions if s().day in days]
        if skip_days:
            solutions = [s for s in solutions if s().day not in skip_days]

        if not solutions:
            self.logger.error("No matching solutions found!")
            return

        if benchmark:
            print(bold("\n=== Advent of Code 2024 Benchmark ==="))
            for solution_class in solutions:
                solution = solution_class()
                results = self.benchmark_solution(solution, benchmark_runs)
                self.print_benchmark_results(solution, results)
                print()  # Add empty line between solutions
        else:
            print(bold("\n=== Advent of Code 2024 ==="))
            for solution_class in solutions:
                solution = solution_class()
                self.run_solution(solution, verbose)


def parse_day_list(day_str: str) -> Set[int]:
    """Parse a comma-separated list of days and day ranges"""
    if not day_str:
        return set()

    days = set()
    for part in day_str.split(','):
        if '-' in part:
            start, end = map(int, part.split('-'))
            days.update(range(start, end + 1))
        else:
            days.add(int(part))
    return days


def main(args=None):
    """
    Run the AOC solutions with the specified arguments.
    If no args provided, parse from command line.
    """
    if args is None:
        parser = argparse.ArgumentParser(description="Advent of Code 2024 Runner")
        parser.add_argument("--days", type=str, help="Days to run (e.g., '1,3-5,7')")
        parser.add_argument("--skip", type=str, help="Days to skip (e.g., '2,6')")
        parser.add_argument("--benchmark", action="store_true", help="Run benchmark")
        parser.add_argument("--benchmark-runs", type=int, default=10,
                            help="Number of benchmark runs")
        parser.add_argument("--verbose", action="store_true", help="Verbose output")
        args = parser.parse_args()

    days = parse_day_list(getattr(args, 'days', None))
    skip_days = parse_day_list(getattr(args, 'skip', None))

    runner = AocRunner()
    runner.run(
        days=days if days else None,
        skip_days=skip_days if skip_days else None,
        benchmark=getattr(args, 'benchmark', False),
        benchmark_runs=getattr(args, 'benchmark_runs', 10),
        verbose=getattr(args, 'verbose', True)
    )


if __name__ == "__main__":
    # Example configurations for easy IDE running:

    # Run all days
    main()

    # Run specific days
    # main(type('Args', (), {'days': '1-5', 'skip': None, 'benchmark': True})())

    # Run all except specific days
    # main(type('Args', (), {'days': None, 'skip': '6,7', 'benchmark': True, 'benchmark_runs': 10})())

    # Benchmark specific days
    # main(type('Args', (), {'days': '7', 'benchmark': True, 'benchmark_runs': 10})())
