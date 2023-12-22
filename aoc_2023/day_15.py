import re
from collections import defaultdict
from pathlib import Path

from aoc_2023.utils import load_input


def hash(text: str) -> int:
    h: int = 0
    for c in text:
        h += ord(c)
        h *= 17
        h %= 256
    return h


def parse(input: str) -> tuple[str, ...]:
    return tuple(input.split(","))


def part1(initialisation_sequence: tuple[str, ...]) -> int:
    hashes: list[int] = [hash(seq) for seq in initialisation_sequence]
    return sum(hashes)


def part2(initialisation_sequence: tuple[str, ...]) -> int:
    boxes: dict[int, list[tuple[str, int]]] = defaultdict(list)
    for step in initialisation_sequence:
        label = re.split("[-=]", step)[0]
        label_hash = hash(label)
        labels_in_box = [lab for lab, _ in boxes[label_hash]]
        if "-" in step:
            if label in labels_in_box:
                pos_in_box = labels_in_box.index(label)
                del boxes[label_hash][pos_in_box]
        elif "=" in step:
            focal_length: int = int(step.split("=")[1])
            if label in labels_in_box:
                pos_in_box = labels_in_box.index(label)
                boxes[label_hash][pos_in_box] = label, focal_length
            else:
                boxes[label_hash].append((label, focal_length))
        else:
            raise ValueError(step)

    scores: list[int] = []
    for box_n, lenses in boxes.items():
        for lens_n, (label, focal_length) in enumerate(lenses):
            scores.append((box_n + 1) * (lens_n + 1) * focal_length)

    return sum(scores)


if __name__ == "__main__":
    day: int = int(Path(__file__).name.split("_")[1].split(".")[0])
    input = load_input(f"example-{day}-1.txt")
    input = load_input(f"input-{day}.txt")
    initialisation_sequence = parse(input)
    print(f"Part 1: {part1(initialisation_sequence)}")
    print(f"Part 2: {part2(initialisation_sequence)}")
