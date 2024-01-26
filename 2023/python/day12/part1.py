import re
from dataclasses import dataclass, field
from typing import Generator
import itertools


class Day12Error(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Puzzle:
    lines: list[str] = field(default_factory=list)
    groups: list[list[int]] = field(default_factory=list)


def valid(line: str, damaged_groups: list[int]) -> bool:
    """Check that line contains groups of # characters
    and that the lengths of the groups matches the
    damaged_groups parameter.
    """
    group_lengths = [len(g) for g in re.findall("#+", line)]

    return group_lengths == damaged_groups


def gen(
    line_with_qmarks: str, expected_springs_count: int
) -> Generator[str, None, None]:
    qindex: list[int] = [i for i, c in enumerate(line_with_qmarks) if c == "?"]
    missing_springs_count = expected_springs_count - line_with_qmarks.count("#")

    for mask in itertools.combinations(range(len(qindex)), missing_springs_count):
        line: list[str] = list(line_with_qmarks)
        for i, j in enumerate(qindex):
            # print(f"{mask=}, {i=}, {j=}")
            if i in mask:
                line[j] = "#"
            else:
                line[j] = "."
        yield "".join(line)


def run(f: str):
    with open(f) as input:
        puzzle = parse(input.read())
        print("Day 12: part 1 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    count = 0
    for line, groups in zip(puzzle.lines, puzzle.groups):
        p = sum(
            (
                1
                for possible_line in gen(line, sum(groups))
                if valid(possible_line, groups)
            )
        )
        # print(f"{line} {p}")
        count += p
    return count


def parse(input: str) -> Puzzle:
    lines = []
    groups = []
    for line in input.splitlines():
        parts = line.split(" ")
        if len(parts) == 2:
            lines.append(parts[0])
            groups.append(list(map(int, parts[1].split(","))))
    return Puzzle(lines, groups)
