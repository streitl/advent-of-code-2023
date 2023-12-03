from collections import defaultdict

import numpy as np
import numpy.typing as npt

from aoc_2023.utils import load_input


def parse_engine(input: str) -> npt.NDArray[str]:
    return np.array([list(line) for line in input.split("\n")])


NEIGHBOR_INDICES: tuple[tuple[int, int], ...] = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def get_all_neighbor_values(
    engine: npt.NDArray[str], row: int, col: int
) -> frozenset[str]:
    nrows, ncols = engine.shape
    return frozenset(
        [
            engine[row + r, col + c]
            for r, c in NEIGHBOR_INDICES
            if 0 <= row + r < nrows and 0 <= col + c < ncols
        ]
    )


base_symbols: frozenset[str] = frozenset(
    [".", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
)


def part1(engine: npt.NDArray[str]) -> int:
    parts_of_sum: list[int] = []
    nrows, ncols = engine.shape
    for r in range(nrows):
        has_neighboring_symbol: bool = False
        curr_n: str = ""
        for c in range(ncols):
            v: str = engine[r, c]
            if v.isdigit():
                curr_n += v
                if len(get_all_neighbor_values(engine, r, c) - base_symbols) > 0:
                    has_neighboring_symbol = True
            else:
                if len(curr_n) > 0 and has_neighboring_symbol:
                    parts_of_sum.append(int(curr_n))
                curr_n = ""
                has_neighboring_symbol = False

        if len(curr_n) > 0 and has_neighboring_symbol:
            parts_of_sum.append(int(curr_n))

    return sum(parts_of_sum)


def part2(engine: npt.NDArray[str]) -> int:
    engine_neighbors: dict[tuple[int, int], list[int]] = defaultdict(list)
    nrows, ncols = engine.shape
    for r in range(nrows):
        neighboring_gears: set[tuple[int, int]] = set()
        curr_n: str = ""
        for c in range(ncols):
            v: str = engine[r, c]
            if v.isdigit():
                curr_n += v
                neighboring_gears.update(
                    [
                        (r + dr, c + dc)
                        for dr, dc in NEIGHBOR_INDICES
                        if 0 <= r + dr < nrows
                        and 0 <= c + dc < ncols
                        and engine[r + dr, c + dc] == "*"
                    ]
                )
            else:
                if len(curr_n) > 0:
                    for gr, gc in neighboring_gears:
                        engine_neighbors[(gr, gc)].append(int(curr_n))
                curr_n = ""
                neighboring_gears.clear()

        if len(curr_n) > 0:
            for gr, gc in neighboring_gears:
                engine_neighbors[(gr, gc)].append(int(curr_n))

    return sum(ns[0] * ns[1] for ns in engine_neighbors.values() if len(ns) == 2)


if __name__ == "__main__":
    engine = parse_engine(load_input("input-03.txt"))
    print(f"Part 1: {part1(engine)}")
    print(f"Part 2: {part2(engine)}")
