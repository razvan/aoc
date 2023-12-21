from dataclasses import dataclass
from typing import List
from itertools import pairwise
from parsy import eof, generate, regex, string, success


@dataclass(frozen=True, slots=True)
class Puzzle:
    history: List[List[int]]


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day 09: part 2 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    return sum([predict(h) for h in puzzle.history])


def predict(history: List[int]) -> int:
    if any(history):
        return history[0] - predict(list(map(lambda t: t[1] - t[0], pairwise(history))))
    else:
        return 0


@generate
def parser():
    number = regex(r"-?\d+").map(int).desc("number")
    padding = regex(r"\s*").desc("padding")
    newline = regex(r"\n").desc("new line")
    singlespace = string(" ")

    history = []
    while True:
        vals = yield padding >> number.sep_by(singlespace) << newline | success(None)
        if not vals:
            break
        history.append(vals)
        yield padding | eof
    return Puzzle(history)
