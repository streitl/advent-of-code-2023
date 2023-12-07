from dataclasses import dataclass

from aoc_2023.utils import load_input


@dataclass
class Draw:
    red: int
    green: int
    blue: int


@dataclass
class Game:
    id: int
    draws: tuple[Draw, ...]


def parse_games(input: str) -> tuple[Game, ...]:
    games = []
    for line in input.split("\n"):
        game_id = int(line.split(":")[0].removeprefix("Game "))
        draws_raw = line.split(": ")[1].split("; ")
        draws = []
        for draw in draws_raw:
            red = 0
            green = 0
            blue = 0
            for part in draw.split(", "):
                ns, color = part.split(" ")
                n = int(ns)
                if color == "red":
                    red = n
                elif color == "green":
                    green = n
                elif color == "blue":
                    blue = n
                else:
                    raise ValueError(f"Unexpected color: {color}")
            draws.append(Draw(red=red, green=green, blue=blue))
        games.append(Game(id=game_id, draws=tuple(draws)))
    return tuple(games)


def part1(games: tuple[Game, ...]):
    return sum(
        game.id
        for game in games
        if all(d.red <= 12 and d.green <= 13 and d.blue <= 14 for d in game.draws)
    )


def part2(games: tuple[Game, ...]):
    return sum(
        max([d.red for d in game.draws])
        * max([d.green for d in game.draws])
        * max([d.blue for d in game.draws])
        for game in games
    )


if __name__ == "__main__":
    games = parse_games(load_input("input-02.txt"))
    print(f"Part 1: {part1(games)}")
    print(f"Part 2: {part2(games)}")
