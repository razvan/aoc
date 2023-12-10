"""
https://adventofcode.com/2023/day/2
"""

import sys
from typing import Iterable, List, Tuple
from .parser import parse
from .model import Game


def possible_games(input: str, total_cubes: Tuple[int, int, int]) -> Iterable[Game]:
    """Return the games that would have been possible given total_cubes."""
    games: List[Game] = parse(input)
    return filter(lambda g: g.max_dice() <= total_cubes, games)


def sum_possible_games(input: str, cubes: Tuple[int, int, int]) -> int:
    return sum(map(lambda g: g.id, possible_games(input, cubes)))


def cube_set_power(input: str) -> int:
    return sum(map(lambda g: g.power(), parse(input)))


def main(f: str):
    with open(f) as input:
        strin = input.read()
        print(
            "Day 02: sum of possible game ids is {0:d}".format(
                sum_possible_games(strin, (12, 13, 14))
            )
        )
        print("Day 02: cube set power is {0:d}".format(cube_set_power(strin)))


if __name__ == "__main__":
    main(sys.argv[1])
