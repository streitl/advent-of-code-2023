from aoc_2023.utils import load_input

LRMapping = dict[str, dict[str, str]]


def parse(input: str) -> tuple[str, LRMapping]:
    main_parts = input.split("\n\n")
    instructions = main_parts[0]
    left_right_mappings = {
        parts[0]: dict(zip(["L", "R"], parts[1][1:-1].split(", ")))
        for line in main_parts[1].split("\n")
        for parts in [line.split(" = ")]
    }
    return instructions, left_right_mappings


def part1(instructions: str, left_right_mappings: LRMapping):
    n_steps = 0
    curr = "AAA"
    while curr != "ZZZ":
        curr = left_right_mappings[curr][instructions[n_steps % len(instructions)]]
        n_steps += 1
    return n_steps


def gcd(a: int, b: int) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)


def part2(instructions: str, left_right_mappings: LRMapping):
    n_steps = 0
    curr_by_pos: dict[int, str] = dict(
        enumerate([node for node in left_right_mappings.keys() if node.endswith("A")])
    )
    cycle_len_by_pos: dict[int, int] = {}
    n_parallel = len(curr_by_pos)
    while len(cycle_len_by_pos) < n_parallel:
        for i in set(curr_by_pos.keys()):
            if curr_by_pos[i].endswith("Z"):
                assert i not in cycle_len_by_pos
                cycle_len_by_pos[i] = n_steps
                del curr_by_pos[i]
            else:
                curr_by_pos[i] = left_right_mappings[curr_by_pos[i]][
                    instructions[n_steps % len(instructions)]
                ]
        n_steps += 1

    cycle_lens = tuple(cycle_len_by_pos.values())
    lcm = cycle_lens[0]
    for n in cycle_lens[1:]:
        lcm = lcm * n // gcd(lcm, n)
    return lcm


if __name__ == "__main__":
    input = load_input("input-08.txt")
    instructions, left_right_mappings = parse(input)
    # print(f"Part 1: {part1(instructions, left_right_mappings)}")
    print(f"Part 2: {part2(instructions, left_right_mappings)}")
