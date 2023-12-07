from dataclasses import dataclass

from aoc_2023.utils import load_input

LEVEL_NAMES: tuple[str, ...] = (
    "seed",
    "soil",
    "fertilizer",
    "water",
    "light",
    "temperature",
    "humidity",
    "location",
)


@dataclass
class SubMappingPart:
    dst: int  # destination
    src: int  # source
    rng: int  # range

    def contains_source(self, i: int) -> bool:
        return self.src <= i < self.src + self.rng

    def contains_destination(self, i: int) -> bool:
        return self.dst <= i < self.dst + self.rng

    def forward(self, i: int) -> int:
        assert self.contains_source(i)
        return self.dst + (i - self.src)

    def backward(self, i: int) -> int:
        assert self.contains_destination(i)
        return self.src + (i - self.dst)


@dataclass
class SubMapping:
    parts: tuple[SubMappingPart, ...]

    def forward(self, i: int) -> int:
        for submapping_part in self.parts:
            if submapping_part.contains_source(i):
                return submapping_part.forward(i)
        return i

    def backward(self, i: int) -> int:
        for submapping_part in self.parts:
            if submapping_part.contains_destination(i):
                return submapping_part.backward(i)
        return i


@dataclass
class Mapping:
    submappings: tuple[SubMapping, ...]

    def forward(self, i: int) -> int:
        for submapping_part in self.submappings:
            i = submapping_part.forward(i)
        return i

    def backward(self, i: int) -> int:
        for submapping_part in self.submappings[::-1]:
            i = submapping_part.backward(i)
        return i


def parse(input: str) -> tuple[tuple[int, ...], Mapping]:
    lines = input.split("\n")
    seeds: tuple[int, ...] = tuple(
        int(i) for i in lines[0].removeprefix("seeds: ").split()
    )
    submappings: list[SubMapping] = []
    curr_submappings_parts: list[SubMappingPart] = []
    for line in [*lines[1:], ""]:
        if line == "" or "map" in line:
            if len(curr_submappings_parts) > 0:
                submappings.append(SubMapping(tuple(curr_submappings_parts)))
                curr_submappings_parts.clear()
            continue
        dst, src, rng = tuple(int(i) for i in line.split())
        curr_submappings_parts.append(SubMappingPart(dst, src, rng))

    assert len(submappings) == len(LEVEL_NAMES) - 1, (
        len(submappings),
        len(LEVEL_NAMES),
    )
    mapping = Mapping(tuple(submappings))
    return seeds, mapping


def part1(seeds: tuple[int, ...], mapping: Mapping) -> int:
    return min(mapping.forward(seed) for seed in seeds)


def part2(seeds: tuple[int, ...], mapping: Mapping):
    seeds_start_range: tuple[tuple[int, int], ...] = tuple(
        zip(seeds[0::2], seeds[1::2])
    )
    location: int = 0
    seed = mapping.backward(location)
    while not any(
        seed_start <= seed < seed_start + seed_range
        for seed_start, seed_range in seeds_start_range
    ):
        location += 1
        seed = mapping.backward(location)
    return location


if __name__ == "__main__":
    seeds, mapping = parse(load_input("input-05.txt"))
    print(f"Part 1: {part1(seeds, mapping)}")
    print(f"Part 2: {part2(seeds, mapping)}")  # Only takes 1 minute!
