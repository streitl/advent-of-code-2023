from aoc_2023.utils import load_input


def part1(input: str) -> int:
    lines = input.split("\n")
    codes: list[int] = []
    for line in lines:
        first, last = None, None
        for char in line:
            if char.isdigit():
                if first is None:
                    first = char
                last = char
        codes.append(int(f"{first}{last}"))
    return sum(codes)


digits: dict[str, int] = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def part2(input: str) -> int:
    lines = input.split("\n")
    codes: list[int] = []
    for line in lines:
        first, last = None, None
        i = 0
        while i < len(line):
            d: int | None = None
            if line[i].isdigit():
                d = int(line[i])
            else:
                for name, val in digits.items():
                    if line[i:].startswith(name):
                        d = val
                        break
            i += 1
            if d is not None:
                if first is None:
                    first = d
                last = d
        code = int(f"{first}{last}")
        codes.append(code)
    return sum(codes)


if __name__ == "__main__":
    input = load_input("input-01.txt")
    print(f"Part 1: {part1(input)}")
    print(f"Part 2: {part2(input)}")
