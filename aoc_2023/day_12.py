from dataclasses import dataclass
from pathlib import Path

from tqdm import tqdm

from aoc_2023.utils import load_input


def is_record_count_valid(record: str, required_counts: tuple[int, ...]) -> bool:
    counts = []
    curr_len = 0
    for r in record + ".":
        if r == "#":
            curr_len += 1
        elif curr_len > 0:
            counts.append(curr_len)
            curr_len = 0
    return tuple(counts) == tuple(required_counts)


@dataclass
class SpringRecord:
    record: str
    checksum: tuple[int, ...]

    def count_arrangements(self) -> int:
        memory: dict[tuple[str, tuple[int, ...]], int] = {}

        def count(record: str, checksum: tuple[int, ...]) -> int:
            if len(record) == 0:
                return int(len(checksum) == 0)
            if len(checksum) == 0:
                return int("#" not in record)
            if (record, checksum) in memory:
                return memory[record, checksum]
            res: int = 0
            if record[0] in ".?":
                res += count(record[1:], checksum)
            if record[0] in "#?":
                if (
                    checksum[0] <= len(record)
                    and "." not in record[: checksum[0]]
                    and (checksum[0] == len(record) or record[checksum[0]] != "#")
                ):
                    res += count(record[checksum[0] + 1 :], checksum[1:])
            memory[record, checksum] = res
            return res

        return count(self.record, self.checksum)


def parse_spring_records(input: str) -> tuple[SpringRecord, ...]:
    return tuple(
        SpringRecord(parts[0], tuple(int(i) for i in parts[1].split(",")))
        for line in input.split("\n")
        for parts in [line.split(" ")]
    )


def part1(spring_records: tuple[SpringRecord, ...]) -> int:
    return sum(record.count_arrangements() for record in tqdm(spring_records))


def part2(spring_records: tuple[SpringRecord, ...], unfolding_rate: int = 5) -> int:
    unfolded_spring_records = tuple(
        SpringRecord(
            "?".join([rec.record] * unfolding_rate),
            rec.checksum * unfolding_rate,
        )
        for rec in spring_records
    )
    return sum(record.count_arrangements() for record in tqdm(unfolded_spring_records))


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    input = load_input(f"example-{day}-1.txt")
    input = load_input(f"input-{day}.txt")
    spring_records = parse_spring_records(input)
    print(f"Part 1: {part1(spring_records)}")
    print(f"Part 2: {part2(spring_records)}")
