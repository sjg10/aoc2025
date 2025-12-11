import importlib
from time import perf_counter


def adventofcode(current_day):
    """
    Run advent of code up to and including current_day
    """
    for day in range(1, current_day + 1):
        module = importlib.import_module(f"days.day{day}")
        run = getattr(module, "run")
        print("\n" + "#" * 32)
        print(f"Day {day}")
        start = perf_counter()
        res = run(open(f"input/day{day}.txt"))
        end = perf_counter()
        print(f"Part 1: {res[0]}")
        print(f"Part 2: {res[1]}")
        print(f"Time elapsed: {(end - start) * 1000:.02f}ms")


if __name__ == "__main__":
    print(f"Advent Of Code 2025")
    adventofcode(11)
