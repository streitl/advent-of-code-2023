from collections import Counter
from dataclasses import dataclass
from typing import Callable

from aoc_2023.utils import load_input

PART_1_CARD_STRENGTHS: tuple[str, ...] = (
    *[str(i) for i in range(2, 10)],
    "T",
    "J",
    "Q",
    "K",
    "A",
)

PART_2_CARD_STRENGTHS: tuple[str, ...] = (
    "J",
    *[str(i) for i in range(2, 10)],
    "T",
    "Q",
    "K",
    "A",
)


@dataclass
class Hand:
    cards: str

    def counts(self) -> Counter[str]:
        return Counter(self.cards)


@dataclass
class Game:
    hand: Hand
    bid: int


GameKey = tuple[tuple[int, ...], ...]


def parse(input: str) -> tuple[Game, ...]:
    return tuple(
        Game(Hand(p[0]), int(p[1]))
        for line in input.split("\n")
        for p in [line.split()]
    )


def get_game_strength(
    counts: dict[str, int], cards: str, cards_ordered_by_strength: tuple[str, ...]
) -> GameKey:
    assert sum(counts.values()) == len(cards)
    decreasing_card_counts = tuple(sorted(counts.values(), reverse=True))
    ordered_hand_strength = tuple(cards_ordered_by_strength.index(c) for c in cards)
    return decreasing_card_counts, ordered_hand_strength


def part_1_game_strength(game: Game) -> GameKey:
    return get_game_strength(
        counts=game.hand.counts(),
        cards=game.hand.cards,
        cards_ordered_by_strength=PART_1_CARD_STRENGTHS,
    )


def part_2_game_strength(game: Game) -> GameKey:
    counts = game.hand.counts()
    decreasing_card_counts = tuple(
        sorted(counts.items(), key=lambda t: t[1], reverse=True)
    )
    for card, count in decreasing_card_counts:
        if card != "J":
            counts[card] += counts["J"]
            counts["J"] = 0
            break
    return get_game_strength(
        counts=counts,
        cards=game.hand.cards,
        cards_ordered_by_strength=PART_2_CARD_STRENGTHS,
    )


def get_winnings(
    games: tuple[Game, ...],
    game_sorting_key: Callable[[Game], GameKey],
) -> int:
    sorted_games = sorted(games, key=game_sorting_key)
    winnings = tuple(g.bid * (rank + 1) for rank, g in enumerate(sorted_games))
    return sum(winnings)


def part1(games: tuple[Game, ...]):
    return get_winnings(games, game_sorting_key=part_1_game_strength)


def part2(games: tuple[Game, ...]):
    return get_winnings(games, game_sorting_key=part_2_game_strength)


if __name__ == "__main__":
    input = load_input("input-07.txt")
    # input = load_input("example-07-1.txt")
    games = parse(input)
    print(f"Part 1: {part1(games)}")
    print(f"Part 2: {part2(games)}")
