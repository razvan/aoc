"""
    Compute the sum of the distances between galaxies by keeping track of the
    universe expansion in terms of offsets from the original positions.

    The brute force attempt (as implementted in part1) ran at 100% cpu for several
    minutes before I stopped it. It also used up ~20GB of memory at the time.

    This implementation doesn't actually expand the original input in any way.
    Instead it computes two lists (one for the x axis and one for the y axis) of
    (start, offset) tuples. The start value represents the start index (in the
    original input) of an expansion and the offset values represent the amount
    of space to add to a coordinate to arrive at the current position.

    This implementaion is general and would also work as the solution for part1
    simply by replacing the expansion factor (times) 1_000_000 with 2.
"""
import re
from dataclasses import dataclass, field
from typing import Generator, Iterable, List, Tuple
from itertools import combinations
from bisect import bisect_right
from parsy import eof, generate, regex, success, whitespace
from operator import attrgetter


class Day11Error(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Puzzle:
    input: List[str]


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day 11: part 2 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    scale_ranges = _expand(puzzle.input, 1_000_000)
    return sum(_dist(combinations(_galaxies(puzzle.input, *scale_ranges), 2)))


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


@dataclass(slots=True, frozen=True, order=True)
class ScaleRange:
    """The index of a row/col of empty space."""

    start: int = field(default=0)
    """The amount if space to add to all coordinates that are greater than start
    to arrive at the current coordinate (after the expansion)."""
    offset: int = field(compare=False, default=0)


def _scale_ranges(axis: Iterable[str], times: int = 2) -> List[ScaleRange]:
    """Compute the ranges of (start,offset) for the given axis."""
    result: List[ScaleRange] = []
    factor: int = 1
    for i, row in enumerate(axis):
        if re.match(r"^\.+$", row):
            result.append(ScaleRange(i, (times - 1) * factor))
            factor += 1
    return result


def _expand(
    input: Iterable[str], times: int = 2
) -> Tuple[List[ScaleRange], List[ScaleRange]]:
    """Compute two lists (one of each coordinate) of offsets."""
    # expand lines
    x_scale = _scale_ranges(input, times)
    # expand cols
    y_scale = _scale_ranges(_transpose(input), times)
    # transpose back
    return (x_scale, y_scale)


def _scale(coord: int, range: List[ScaleRange]) -> int:
    """Scale an original coordinate value (x or y) to arrive at the current
    position.

    It is assumed that the range list is sorted (by the start attribute) and
    uses the bisect_right() function to find the largest start index that is
    smaller than coord and adds the corresponding offset to coord.

    If no start index is found, the coordinate is in the first qudrant where
    no expansion has happened.
    """
    attrscale = attrgetter("start")
    index = bisect_right(range, coord, key=attrscale)
    if index:
        # print(f"{coord=} {range[index - 1]}")
        return coord + range[index - 1].offset
    else:
        return coord


def _galaxies(
    input: Iterable[str], x_scale: List[ScaleRange], y_scale: List[ScaleRange]
) -> Generator[Tuple[int, int], None, None]:
    """Return the current coordinates of the galaxies after the universe
    expansion."""
    for i, row in enumerate(input):
        for j, dot in enumerate(row):
            if dot == "#":
                yield (_scale(i, x_scale), _scale(j, y_scale))


def _dist(
    input: Iterable[Tuple[Tuple[int, int], Tuple[int, int]]],
) -> Generator[int, None, None]:
    """Return the distances between each pair of galaxies (input)."""
    for gs in input:
        yield abs(gs[0][0] - gs[1][0]) + abs(gs[0][1] - gs[1][1])
