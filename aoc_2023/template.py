from pathlib import Path

from aoc_2023.utils import load_input


def part1():
    pass


def part2():
    pass


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    input = load_input(f"example-{day}-1.txt")
    input = load_input(f"input-{day}.txt")
    print(f"Part 1: {part1()}")
    print(f"Part 2: {part2()}")
