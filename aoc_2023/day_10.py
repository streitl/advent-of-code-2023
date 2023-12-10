from pathlib import Path

import numpy as np
import numpy.typing as npt

from aoc_2023.utils import load_input

Point = tuple[int, int]

WEST: tuple[int, int] = 0, -1
EAST: tuple[int, int] = 0, 1
NORTH: tuple[int, int] = -1, 0
SOUTH: tuple[int, int] = 1, 0

PIPE_TO_DIRECTION: dict[str, set[tuple[int, int]]] = {
    ".": set(),
    "|": {NORTH, SOUTH},
    "-": {WEST, EAST},
    "L": {NORTH, EAST},
    "J": {NORTH, WEST},
    "F": {SOUTH, EAST},
    "7": {SOUTH, WEST},
}

LEFT_ROTATION_MATRIX: npt.NDArray[np.int_] = np.array([[0, -1], [1, 0]])
RIGHT_ROTATION_MATRIX: npt.NDArray[np.int_] = np.array([[0, 1], [-1, 0]])


def in_map(*, point: tuple[int, int], pipes: npt.NDArray[np.object_]) -> bool:
    y, x = point
    ymax, xmax = pipes.shape
    return 0 <= x < xmax and 0 <= y < ymax


def get_pipe_connections(
    pos: Point, pipes: npt.NDArray[np.object_]
) -> frozenset[Point]:
    y, x = pos
    pipe = str(pipes[y, x])

    neighbors = frozenset(
        {
            (y + dy, x + dx)
            for dy, dx in PIPE_TO_DIRECTION[pipe]
            if in_map(point=(y + dy, x + dx), pipes=pipes)
        }
    )
    return neighbors


def get_all_pipe_connections(
    *, pipes: npt.NDArray[np.object_], S_pos: Point
) -> dict[Point, frozenset[Point]]:
    ymax, xmax = pipes.shape
    pipe_connections: dict[Point, frozenset[Point]] = {
        (y, x): get_pipe_connections((y, x), pipes)
        for y in range(ymax)
        for x in range(xmax)
        if (y, x) != S_pos
    }
    pipe_connections[S_pos] = frozenset(
        {pos for pos, neighbors in pipe_connections.items() if S_pos in neighbors}
    )
    assert len(pipe_connections[S_pos]) == 2
    return pipe_connections


def parse(input: str) -> npt.NDArray[np.object_]:
    return np.array([list(line) for line in input.split("\n")])


def spread_seeds(
    *, seeds: set[Point], pipes: npt.NDArray[np.object_], loop: frozenset[Point]
) -> frozenset[Point]:
    explored: set[Point] = set()
    to_explore: set[Point] = {s for s in seeds}
    while len(to_explore) > 0:
        ey, ex = to_explore.pop()
        explored.add((ey, ex))
        for dy, dx in (
            NORTH,
            EAST,
            SOUTH,
            WEST,
        ):
            ny, nx = (ey + dy, ex + dx)
            if (
                in_map(point=(ny, nx), pipes=pipes)
                and (ny, nx) not in loop
                and (ny, nx) not in explored
            ):
                to_explore.add((ny, nx))
    return frozenset(explored)


def find_loop_and_left_right(
    *,
    S_pos: Point,
    pipe_connections: dict[Point, frozenset[Point]],
    pipes: npt.NDArray[np.object_],
) -> tuple[frozenset[Point], frozenset[Point], frozenset[Point]]:
    curr = next(iter(pipe_connections[S_pos]))
    loop: set[Point] = {S_pos}
    while len(possible := (pipe_connections[curr] - loop)) > 0:
        loop.add(curr)
        curr = next(iter(possible))
    loop.add(curr)

    left_seeds: set[Point] = set()
    right_seeds: set[Point] = set()
    curr = S_pos
    seen: set[Point] = set()
    while len(possible := (pipe_connections[curr] - seen)) > 0:
        seen.add(curr)
        prev = curr
        curr = next(iter(possible))
        diff = np.array(curr) - np.array(prev)
        for set_to_add, rotation_matrix in zip(
            [left_seeds, right_seeds], [LEFT_ROTATION_MATRIX, RIGHT_ROTATION_MATRIX]
        ):
            for point in [curr, prev]:
                neighbor: Point = tuple(np.array(point) + rotation_matrix @ diff)
                if in_map(point=neighbor, pipes=pipes) and neighbor not in loop:
                    set_to_add.add(neighbor)

    left_grown = spread_seeds(seeds=left_seeds, pipes=pipes, loop=frozenset(loop))
    right_grown = spread_seeds(seeds=right_seeds, pipes=pipes, loop=frozenset(loop))
    left = left_seeds | left_grown
    right = right_seeds | right_grown
    assert len(left & right) == 0, left & right
    assert len(left) + len(right) + len(loop) == pipes.shape[0] * pipes.shape[1], (
        f"{len(left)} + {len(right)} + {len(loop)} = {len(left) + len(right) + len(loop)},"
        f" not {pipes.shape[0] * pipes.shape[1]}"
    )
    return frozenset(loop), frozenset(left), frozenset(right)


def part1(*, loop: frozenset[Point]):
    n = len(loop)
    return (n // 2) + n % 2


def part2(*, left: frozenset[Point], right: frozenset[Point]) -> tuple[int, int]:
    return len(left), len(right)


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    input = load_input(f"example-{day}-5.txt")
    input = load_input(f"input-{day}.txt")
    pipes = parse(input)
    S_pos: Point = tuple(np.ravel(np.where(pipes == "S")))
    pipe_connections = get_all_pipe_connections(pipes=pipes, S_pos=S_pos)
    loop, left, right = find_loop_and_left_right(
        S_pos=S_pos, pipe_connections=pipe_connections, pipes=pipes
    )
    print(f"Part 1: {part1(loop=loop)}")
    print(f"Part 2: {part2(left=left, right=right)}")
