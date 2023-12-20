from dataclasses import dataclass
from typing import Dict, Tuple
from itertools import cycle

from parsy import eof, generate, regex, string, whitespace, success


@dataclass(frozen=True, slots=True)
class Puzzle:
    # directions. A string of L (left) an R (right) instructions.
    dirs: str
    # Start location. Always "AAA"
    start: str
    # Mapping between a start location and two possible next locations,
    # left and right.
    locs: Dict[str, Tuple[str, str]]


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day 08: part 1 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    """Returns the number of "moves" (left and right) are required
    to arrive from the start location ("AAA") and arrive to the
    final location ("ZZZ").
    """
    loc = puzzle.start
    moves = 0
    for dir in cycle(puzzle.dirs):
        if loc == "ZZZ":
            break
        loc = next_loc(dir, puzzle.locs[loc])
        moves += 1

    return moves


def next_loc(dir: str, locs: Tuple[str, str]) -> str:
    if dir == "L":
        return locs[0]
    else:
        return locs[1]


@generate
def parser():
    padding = regex(r"\s*")
    lparen = string("(")
    rparen = string(")")
    equals = string("=")
    comma = string(",")
    direction = regex(r"[LR]+")
    location = regex(r"[A-Z]{3}")

    locs: Dict[str, Tuple[str, str]] = {}
    dir = yield padding >> direction << whitespace
    while True:
        loc = yield padding >> location << whitespace | success(None)
        if not loc:
            break
        yield equals.desc("equals sign") >> whitespace >> lparen.desc("left paren")
        left = yield location.desc("left")
        yield comma >> whitespace
        right = yield location.desc("right")
        yield rparen.desc("right paren") >> (padding | eof)
        locs[loc] = (left, right)

    return Puzzle(dir, "AAA", locs)
