import math
from dataclasses import dataclass
from itertools import cycle
from typing import Dict, Iterable, List, Tuple

from parsy import eof, generate, regex, string, success, whitespace


@dataclass(frozen=True, slots=True)
class Puzzle:
    dirs: str
    locs: Dict[str, Tuple[str, str]]


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day 08: part 2 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    return solve_lcm(puzzle)
    # return solve_brute_force(puzzle)


def solve_lcm(puzzle: Puzzle) -> int:
    """Compute the amount of moves for every start location and
    return the least common multiplyer of them."""
    all_moves: List[int] = []
    locs = find_start_loc(puzzle.locs.keys())
    for loc in locs:
        moves: int = 0
        for dir in cycle(puzzle.dirs):
            if loc.endswith("Z"):
                break
            loc = next_loc(dir, [loc], puzzle.locs)[0]
            moves += 1
        all_moves.append(moves)

    return math.lcm(*all_moves)


def solve_brute_force(puzzle: Puzzle) -> int:
    """This attempt uses brute force. It didn't complete in a reasonable
    amount of time."""
    loc = find_start_loc(puzzle.locs.keys())
    moves = 0
    for dir in cycle(puzzle.dirs):
        if is_end_loc(loc):
            break
        loc = next_loc(dir, loc, puzzle.locs)
        moves += 1

    return moves


def find_start_loc(locs: Iterable[str]) -> List[str]:
    return [location for location in locs if location.endswith("A")]


def is_end_loc(loc: List[str]) -> bool:
    return all((location.endswith("Z") for location in loc))


def next_loc(dir: str, start: List[str], locs: Dict[str, Tuple[str, str]]) -> List[str]:
    if dir == "L":
        return [locs[s][0] for s in start]
    else:
        return [locs[s][1] for s in start]


@generate
def parser():
    padding = regex(r"\s*")
    lparen = string("(")
    rparen = string(")")
    equals = string("=")
    comma = string(",")
    direction = regex(r"[LR]+")
    location = regex(r"[0-9A-Z]{3}")

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

    return Puzzle(dir, locs)
