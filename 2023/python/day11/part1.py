import re
from dataclasses import dataclass
from typing import Generator, Iterable, List, Tuple
from itertools import combinations

from parsy import eof, generate, regex, success, whitespace


class DayXXError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Puzzle:
    input: List[str]


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day 11: part 1 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    return sum(_dist(combinations(_galaxies(_expand(puzzle.input)), 2)))


@generate
def parser():
    padding = regex(r"\s*")
    dots = []
    yield padding
    while True:
        row = yield regex("[.#]+") | success(None)
        if not row:
            break
        dots.append(row)
        yield whitespace
    yield padding | eof
    return Puzzle(dots)


def _transpose(input: Iterable[str]) -> Iterable[str]:
    return map("".join, zip(*input))


def _duplicate(input: Iterable[str]) -> Generator[str, None, None]:
    for row in input:
        if re.match(r"^\.+$", row):
            yield row
            yield row
        else:
            yield row


def _expand(input: Iterable[str]) -> List[str]:
    # expand lines
    tmp = _duplicate(input)
    # expand cols
    tmp = _duplicate(_transpose(tmp))
    # transpose back
    return list(_transpose(tmp))


def _galaxies(input: Iterable[str]) -> Generator[Tuple[int, int], None, None]:
    for i, row in enumerate(input):
        for j, dot in enumerate(row):
            if dot == "#":
                yield (i, j)


def _dist(
    input: Iterable[Tuple[Tuple[int, int], Tuple[int, int]]],
) -> Generator[int, None, None]:
    for gs in input:
        yield abs(gs[0][0] - gs[1][0]) + abs(gs[0][1] - gs[1][1])
