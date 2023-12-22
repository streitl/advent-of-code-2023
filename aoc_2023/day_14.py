from pathlib import Path

import numpy as np
import numpy.typing as npt

from aoc_2023.utils import load_input


def parse(input: str) -> npt.NDArray[np.str_]:
    return np.array([list(line) for line in input.split("\n")])


def slide_north(
    rocks: npt.NDArray[np.str_],
) -> npt.NDArray[np.str_]:
    nrows, ncols = rocks.shape
    slided = rocks.copy()
    for row in range(nrows):
        for col in range(ncols):
            if slided[row, col] == "O":
                upper_row = row - 1
                while upper_row >= 0 and slided[upper_row, col] == ".":
                    upper_row -= 1
                (slided[upper_row + 1, col], slided[row, col]) = (
                    slided[row, col],
                    slided[upper_row + 1, col],
                )
    return slided


def get_north_load(rocks: npt.NDArray[np.str_]) -> int:
    nrows, ncols = rocks.shape
    loads: list[int] = []
    for row in range(nrows):
        for col in range(ncols):
            if rocks[row, col] == "O":
                loads.append(nrows - row)
    return sum(loads)


def part1(rocks: npt.NDArray[np.str_]):
    slided = slide_north(rocks)
    load = get_north_load(slided)
    return load


def show(rocks: npt.NDArray[np.str_]) -> None:
    nrows, ncols = rocks.shape
    print(" " + "-" * ncols + " ")
    for row in rocks:
        print("|" + "".join(row) + "|")
    print(" " + "-" * ncols + " ")


def apply_spin(rocks: npt.NDArray[np.str_]) -> npt.NDArray[np.str_]:
    rocks = slide_north(rocks)
    rocks = np.rot90(slide_north(np.rot90(rocks, k=-1)), k=1)
    rocks = np.rot90(slide_north(np.rot90(rocks, k=-2)), k=2)
    rocks = np.rot90(slide_north(np.rot90(rocks, k=-3)), k=3)
    return rocks


def part2(rocks: npt.NDArray[np.str_], n_spins: int = 1_000_000_000):
    rocks = rocks.copy()
    last_occurrence: dict[tuple[tuple[str, ...], ...], int] = dict()
    for spin in range(n_spins):
        rocks = apply_spin(rocks)
        tupled_rocks = tuple(tuple(line) for line in rocks)
        if tupled_rocks in last_occurrence:
            cycle_size = spin - last_occurrence[tupled_rocks]
            remaining_spins = n_spins - spin - 1
            for extra_spin in range(remaining_spins % cycle_size):
                rocks = apply_spin(rocks)
            return get_north_load(rocks)
        last_occurrence[tupled_rocks] = spin
    return get_north_load(rocks)


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    # input = load_input(f"example-{day}-1.txt")
    input = load_input(f"input-{day}.txt")
    rocks = parse(input)
    print(f"Part 1: {part1(rocks)}")
    print(f"Part 2: {part2(rocks)}")
