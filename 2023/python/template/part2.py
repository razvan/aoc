import re
from dataclasses import dataclass

from parsy import generate, regex


class DayXXError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Puzzle:
    pass


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day xx: part 2 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    return 2


@generate
def parser():
    yield regex(".*", re.DOTALL)
    return Puzzle()
