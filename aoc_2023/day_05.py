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
class SubMapping:
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
class Mapping:
    submappings: tuple[SubMapping, ...]

    def forward(self, i: int) -> int:
        for submapping in self.submappings:
            if submapping.contains_source(i):
                return submapping.forward(i)
        return i

    def backward(self, i: int) -> int:
        for submapping in self.submappings:
            if submapping.contains_destination(i):
                return submapping.backward(i)
        return i


def parse(input: str) -> tuple[tuple[int, ...], tuple[Mapping, ...]]:
    lines = input.split("\n")
    seeds: tuple[int, ...] = tuple(
        int(i) for i in lines[0].removeprefix("seeds: ").split()
    )
    mappings: list[Mapping] = []
    curr_submappings: list[SubMapping] = []
    for line in [*lines[1:], ""]:
        if line == "" or "map" in line:
            if len(curr_submappings) > 0:
                mappings.append(Mapping(tuple(curr_submappings)))
                curr_submappings.clear()
            continue
        dst, src, rng = tuple(int(i) for i in line.split())
        curr_submappings.append(SubMapping(dst, src, rng))

    assert len(mappings) == len(LEVEL_NAMES) - 1, (len(mappings), len(LEVEL_NAMES))
    return seeds, tuple(mappings)


def part1(seeds: tuple[int, ...], mappings: tuple[Mapping, ...]) -> int:
    min_result: int | None = None
    for seed in seeds:
        curr = seed
        for mapping in mappings:
            curr = mapping.forward(curr)
        if min_result is None or curr < min_result:
            min_result = curr
    return min_result


def part2(seeds: tuple[int, ...], mappings: tuple[Mapping, ...]):
    seed_submapping = tuple(
        SubMapping(dst=start, src=start, rng=rng)
        for start, rng in zip(seeds[0::2], seeds[1::2])
    )
    location: int = 0
    while True:
        curr = location
        for mapping in mappings[::-1]:
            curr = mapping.backward(curr)
        if any(submapping.contains_source(curr) for submapping in seed_submapping):
            break
        location += 1
    return location


if __name__ == "__main__":
    seeds, mappings = parse(load_input("input-05.txt"))
    print(f"Part 1: {part1(seeds, mappings)}")
    print(f"Part 2: {part2(seeds, mappings)}")  # Only takes 1 minute!
