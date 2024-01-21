import re
from dataclasses import dataclass, field
from typing import Generator


class Day12Error(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Puzzle:
    lines: dict[str, list[int]] = field(default_factory=dict)


def valid(line: str, damaged_groups: list[int]) -> bool:
    """Check that line contains groups of # characters
    and that the lengths of the groups matches the
    damaged_groups parameter.
    """
    group_lengths = [len(g) for g in re.findall("#+", line)]

    return group_lengths == damaged_groups


def gen(line_with_qmarks: str) -> Generator[str, None, None]:
    qindex: list[int] = [i for i, c in enumerate(line_with_qmarks) if c == "?"]

    for mask in range(1 << len(qindex)):
        line: list[str] = list(line_with_qmarks)
        for i, j in enumerate(qindex):
            if mask & (1 << i):
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
    for line, groups in puzzle.lines.items():
        for possible_line in gen(line):
            if valid(possible_line, groups):
                count += 1
    return count


def parse(input: str) -> Puzzle:
    result: dict[str, list[int]] = {}
    for line in input.splitlines():
        parts = line.split(" ")
        if len(parts) == 2:
            result[parts[0]] = [int(c) for c in parts[1].split(",")]
    return Puzzle(result)
