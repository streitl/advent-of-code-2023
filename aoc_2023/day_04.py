from aoc_2023.utils import load_input


def get_n_common_numbers(card: str) -> int:
    card = card.split(":")[1]
    winning, own = card.split(" | ")
    winning_numbers = set(int(s) for s in winning.split())
    own_numbers = set(int(s) for s in own.split())
    return len(winning_numbers & own_numbers)


def part1(input: str) -> int:
    total: int = 0
    for card in input.split("\n"):
        n_common = get_n_common_numbers(card)
        score = 2 ** (n_common - 1) if n_common != 0 else 0
        total += score
    return total


def part2(input: str) -> int:
    all_cards = input.split("\n")
    n_cards = [1 for _ in range(len(all_cards))]
    for curr_i, card in enumerate(all_cards):
        n_common = get_n_common_numbers(card)
        for i in range(n_common):
            next_i = curr_i + i + 1
            n_cards[next_i] += n_cards[curr_i]
    return sum(n_cards)


if __name__ == "__main__":
    input = load_input("input-04.txt")
    print(f"Part 1: {part1(input)}")
    print(f"Part 2: {part2(input)}")
