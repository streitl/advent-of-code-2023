from dataclasses import dataclass
from functools import reduce

import numpy as np

from aoc_2023.utils import load_input


@dataclass
class Race:
    time: int
    distance_record: int


Races = tuple[Race, ...]


def get_numbers_after_prefix(input: str, prefix: str) -> tuple[int, ...]:
    return tuple(int(i) for i in input.removeprefix(prefix).strip().split())


def parse(input: str) -> Races:
    lines = [line for line in input.split("\n") if len(line) > 0]
    assert len(lines) == 2, lines
    times = get_numbers_after_prefix(lines[0], "Time:")
    records = get_numbers_after_prefix(lines[1], "Distance:")
    assert len(times) == len(records)
    return tuple(Race(t, d) for t, d in zip(times, records))


def part1(races: Races):
    scores: list[int] = []
    for race in races:
        possible_speeds = np.arange(1, race.time)
        possible_distances = possible_speeds * (race.time - possible_speeds)
        is_record_break = possible_distances > race.distance_record
        n_record_breaks = is_record_break.sum()
        scores.append(n_record_breaks)
    return reduce(lambda a, b: a * b, scores, 1)


def part2(races: Races):
    real_race: Race = Race(
        time=int(reduce(lambda a, b: f"{a}{b}", [r.time for r in races], "")),
        distance_record=int(
            reduce(lambda a, b: f"{a}{b}", [r.distance_record for r in races], "")
        ),
    )
    return part1((real_race,))


if __name__ == "__main__":
    input = load_input("input-06.txt")
    races = parse(input)
    print(f"Part 1: {part1(races)}")
    print(f"Part 2: {part2(races)}")
