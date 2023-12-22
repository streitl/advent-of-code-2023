import dataclasses
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import numpy.typing as npt
from tqdm import tqdm

from aoc_2023.utils import load_input


def parse(input: str) -> npt.NDArray[np.str_]:
    return np.array([list(line) for line in input.split("\n")])


NORTH: tuple[int, int] = (-1, 0)
EAST: tuple[int, int] = (0, 1)
SOUTH: tuple[int, int] = (1, 0)
WEST: tuple[int, int] = (0, -1)


@dataclass(frozen=True)
class Beam:
    position: tuple[int, int]
    direction: tuple[int, int]


def count_energy(grid: npt.NDArray[np.str_], starting_beam: Beam) -> int:
    nrows, ncols = grid.shape
    curr_beams: set[Beam] = {starting_beam}
    seen_beams: set[Beam] = curr_beams.copy()
    energized_cells: set[tuple[int, int]] = set()
    while len(curr_beams) > 0:
        new_beams: set[Beam] = set()
        for old_beam in curr_beams:
            beam = dataclasses.replace(
                old_beam,
                position=(
                    old_beam.position[0] + old_beam.direction[0],
                    old_beam.position[1] + old_beam.direction[1],
                ),
            )
            if not (0 <= beam.position[0] < nrows and 0 <= beam.position[1] < ncols):
                continue
            energized_cells.add(beam.position)
            if grid[beam.position] == ".":
                new_beams.add(beam)
            elif grid[beam.position] == "/":
                new_beams.add(
                    dataclasses.replace(
                        beam,
                        direction=NORTH
                        if beam.direction == EAST
                        else EAST
                        if beam.direction == NORTH
                        else WEST
                        if beam.direction == SOUTH
                        else SOUTH,
                    )
                )
            elif grid[beam.position] == "\\":
                new_beams.add(
                    dataclasses.replace(
                        beam,
                        direction=NORTH
                        if beam.direction == WEST
                        else WEST
                        if beam.direction == NORTH
                        else EAST
                        if beam.direction == SOUTH
                        else SOUTH,
                    )
                )
            elif grid[beam.position] == "|":
                if beam.direction == NORTH or beam.direction == SOUTH:
                    new_beams.add(beam)
                else:
                    new_beams.add(dataclasses.replace(beam, direction=NORTH))
                    new_beams.add(dataclasses.replace(beam, direction=SOUTH))
            elif grid[beam.position] == "-":
                if beam.direction == WEST or beam.direction == EAST:
                    new_beams.add(beam)
                else:
                    new_beams.add(dataclasses.replace(beam, direction=EAST))
                    new_beams.add(dataclasses.replace(beam, direction=WEST))
        curr_beams = new_beams - seen_beams
        seen_beams |= curr_beams

    return len(energized_cells)


def part1(grid: npt.NDArray[np.str_]) -> int:
    return count_energy(grid, starting_beam=Beam(position=(0, -1), direction=EAST))


def part2(grid: npt.NDArray[np.str_]) -> int:
    nrows, ncols = grid.shape
    starting_beams = (
        {Beam(position=(-1, x), direction=SOUTH) for x in range(ncols)}
        | {Beam(position=(nrows, x), direction=NORTH) for x in range(ncols)}
        | {Beam(position=(y, -1), direction=EAST) for y in range(nrows)}
        | {Beam(position=(y, ncols), direction=WEST) for y in range(nrows)}
    )
    energy_per_starting_beam = {
        beam: count_energy(grid, starting_beam=beam) for beam in tqdm(starting_beams)
    }
    return max(energy_per_starting_beam.values())


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    input = load_input(f"example-{day}-1.txt")
    input = load_input(f"input-{day}.txt")
    grid = parse(input)
    print(f"Part 1: {part1(grid)}")
    print(f"Part 2: {part2(grid)}")
