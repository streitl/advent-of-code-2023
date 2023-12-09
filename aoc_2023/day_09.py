from aoc_2023.utils import load_input


def compute_diffs_per_level(history: list[int]) -> list[list[int]]:
    current = history
    diffs_per_level: list[list[int]] = [history]
    while len(diffs := [a - b for a, b in zip(current[1:], current)]) > 0 and not all(
        d == 0 for d in diffs
    ):
        current = diffs
        diffs_per_level.append(diffs)
    return diffs_per_level


def part1(histories: list[list[int]]) -> int:
    next_values: list[int] = []
    for history in histories:
        diffs_per_level = compute_diffs_per_level(history)
        for level in range(len(diffs_per_level) - 1, 0, -1):
            diffs_per_level[level - 1].append(
                diffs_per_level[level - 1][-1] + diffs_per_level[level][-1]
            )
        next_values.append(diffs_per_level[0][-1])
    return sum(next_values)


def part2(histories: list[list[int]]) -> int:
    previous_values: list[int] = []
    for history in histories:
        diffs_per_level = compute_diffs_per_level(history)
        for level in range(len(diffs_per_level) - 1, 0, -1):
            diffs_per_level[level - 1].insert(
                0, diffs_per_level[level - 1][0] - diffs_per_level[level][0]
            )
        previous_values.append(diffs_per_level[0][0])
    return sum(previous_values)


def parse(input: str) -> list[list[int]]:
    return [[int(el) for el in line.split()] for line in input.split("\n")]


if __name__ == "__main__":
    input = load_input("input-09.txt")
    histories = parse(input)
    print(f"Part 1: {part1(histories)}")
    print(f"Part 2: {part2(histories)}")
