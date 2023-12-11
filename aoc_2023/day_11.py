from pathlib import Path

import numpy as np
import numpy.typing as npt

from aoc_2023.utils import load_input


def parse(input: str) -> npt.NDArray[np.str_]:
    return np.array([list(line) for line in input.split("\n")])


def find_distance_between_all_galaxies(
    sky: npt.NDArray[np.str_], expansion_rate: int
) -> tuple[int, ...]:
    n_rows, n_cols = sky.shape
    galaxies = np.argwhere(sky == "#")
    rows_with_galaxies = set(y for y, x in galaxies)
    cols_with_galaxies = set(x for y, x in galaxies)
    empty_rows = set(range(n_rows)) - rows_with_galaxies
    empty_cols = set(range(n_cols)) - cols_with_galaxies
    distances: list[int] = []
    for i, (ya, xa) in enumerate(galaxies):
        for j, (yb, xb) in enumerate(galaxies):
            if j <= i:
                continue
            rows_in_between = set(range(min(ya, yb), max(ya, yb)))
            cols_in_between = set(range(min(xa, xb), max(xa, xb)))

            distance = (
                len(cols_in_between - empty_cols)
                + len(rows_in_between - empty_rows)
                + expansion_rate
                * (
                    len(empty_cols & cols_in_between)
                    + len(empty_rows & rows_in_between)
                )
            )
            distances.append(distance)
    return tuple(distances)


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    input = load_input(f"input-{day}.txt")
    sky = parse(input)
    print(f"Part 1: {sum(find_distance_between_all_galaxies(sky, expansion_rate=2))}")
    print(
        f"Part 2: {sum(find_distance_between_all_galaxies(sky, expansion_rate=1000000))}"
    )
