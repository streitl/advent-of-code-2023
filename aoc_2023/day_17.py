from collections import defaultdict
from pathlib import Path

import numpy as np
import numpy.typing as npt

from aoc_2023.utils import load_input

Point = tuple[int, int]
Direction = tuple[int, int]

NORTH: Direction = (-1, 0)
EAST: Direction = (0, 1)
SOUTH: Direction = (1, 0)
WEST: Direction = (0, -1)


def parse(input: str) -> npt.NDArray[np.int_]:
    return np.array([list(line) for line in input.split("\n")]).astype(int)


def find_last_n_directions(
    point: Point, previous: dict[Point, Point], n: int
) -> frozenset[Direction]:
    last_three_directions: list[Direction] = []
    curr = point
    for i in range(n):
        prev = previous[curr]
        last_three_directions.append((curr[0] - prev[0], curr[1] - prev[1]))
        curr = prev
    print(point, last_three_directions)
    return frozenset(last_three_directions)


def retrieve_path_to(point: Point, previous: dict[Point, Point]) -> list[Point]:
    curr = point
    path = [point]
    while curr != previous[curr]:
        curr = previous[curr]
        path.append(curr)
    return path[::-1]


def find_path(city: npt.NDArray[np.int_]) -> int:
    nrows, ncols = city.shape
    start: Point = (0, 0)
    goal: Point = (nrows - 1, ncols - 1)

    distance: dict[Point, float] = defaultdict(lambda: float("inf")) | {start: 0}
    unvisited: set[Point] = set((y, x) for y in range(nrows) for x in range(ncols))
    previous: dict[Point, Point] = {start: start}

    while goal in unvisited:
        cy, cx = min(unvisited, key=lambda p: distance[p])
        unvisited.remove((cy, cx))

        (py, px) = previous[cy, cx]
        backward_direction = (py - cy, px - cx)
        allowed_directions = {NORTH, EAST, SOUTH, WEST} - {backward_direction}
        last_three_directions = find_last_n_directions((cy, cx), previous, n=3)
        if len(last_three_directions) == 1:
            allowed_directions -= last_three_directions
        for dy, dx in allowed_directions:
            ny, nx = (cy + dy, cx + dx)
            if 0 <= ny < nrows and 0 <= nx < ncols and (ny, nx) in unvisited:
                new_distance = distance[cy, cx] + city[ny, nx]
                if (ny, nx) not in distance or new_distance < distance[ny, nx]:
                    distance[ny, nx] = new_distance
                    previous[ny, nx] = (cy, cx)
    shortest_path = retrieve_path_to(goal, previous)
    grid = np.full(shape=city.shape, fill_value=".")
    for py, px in shortest_path:
        grid[py, px] = "#"
    print(grid)
    for y, x in [(0, 1), (1, 0)]:
        print(y, x, distance[y, x])
    return int(distance[goal])


def part1(city: npt.NDArray[np.int_]) -> int:
    return find_path(city)


def part2(city: npt.NDArray[np.int_]):
    pass


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    input = load_input(f"example-{day}-1.txt")
    # input = load_input(f"input-{day}.txt")
    city = parse(input)
    print(f"Part 1: {part1(city)}")
    print(f"Part 2: {part2(city)}")
