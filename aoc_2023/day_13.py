from pathlib import Path

import numpy as np
import numpy.typing as npt

from aoc_2023.utils import load_input

MirrorField = npt.NDArray[np.str_]


def parse(input: str) -> tuple[MirrorField, ...]:
    return tuple(
        np.array([[el for el in line] for line in part.split("\n")])
        for part in input.split("\n\n")
    )


def find_reflections(mirror_fields: tuple[MirrorField, ...], n_smudges: int) -> int:
    summaries: list[int] = []
    for field in mirror_fields:
        nrows, ncols = field.shape
        # Horizontal reflection
        for row in range(1, nrows):
            min_size = min(row, nrows - row)
            left = field[row - min_size : row]
            right = field[row : row + min_size, :]
            if np.sum(left != np.flip(right, axis=0)) == n_smudges:
                summaries.append(100 * row)
                break
        # Vertical reflection
        for col in range(1, ncols):
            min_size = min(col, ncols - col)
            above = field[:, col - min_size : col]
            below = field[:, col : col + min_size]
            if np.sum(above != np.flip(below, axis=1)) == n_smudges:
                summaries.append(col)
                break
    return sum(summaries)


def part1(mirror_fields: tuple[MirrorField, ...]) -> int:
    return find_reflections(mirror_fields, n_smudges=0)


def part2(mirror_fields: tuple[MirrorField, ...]) -> int:
    return find_reflections(mirror_fields, n_smudges=1)


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    # input = load_input(f"example-{day}-1.txt")
    input = load_input(f"input-{day}.txt")
    mirror_fields = parse(input)
    print(f"Part 1: {part1(mirror_fields)}")
    print(f"Part 2: {part2(mirror_fields)}")
