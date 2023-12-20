import re
from dataclasses import dataclass
from typing import List

from parsy import generate, regex


@dataclass(frozen=True, slots=True)
class Puzzle:
    pass


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day xx: part 1 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    return 1


@generate
def parser():
    yield regex(".*", re.DOTALL)
    return Puzzle()
