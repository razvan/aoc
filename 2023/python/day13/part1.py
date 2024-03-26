from dataclasses import dataclass

from typing import List


class Day13Error(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Puzzle:
    patterns: List[List[str]]


def run(f: str):
    with open(f) as input:
        p: List[str] = []
        patts: List[List[str]] = []
        for line in input.read().splitlines():
            if line:
                p.append(line)
            else:
                patts.append(p)
                p = []
        if p:
            patts.append(p)

        print("Day 13: part 1 is {}".format(solve(Puzzle(patts))))


def solve(puzzle: Puzzle) -> int:
    return sum(map(lines_before_mirror, puzzle.patterns))


def transpose(input: List[str]) -> list[str]:
    if not input:
        return []
    else:
        maxlen = max(map(len, input))
        return [
            "".join([row[i] for row in input if i < len(row)]) for i in range(maxlen)
        ]


def lines_before_mirror(input: List[str]) -> int:
    result = _mirror_index(input)
    if result is None:
        result = _mirror_index(transpose(input))
        if result is None:
            raise Day13Error(f"No mirror found for pattern:\n{'\n'.join(input)}")
        else:
            return result
    else:
        return result * 100


def _mirror_index(input: List[str]) -> int | None:
    if len(input) < 2:
        return None
    for i in range(1, len(input)):
        if input[i - 1] == input[i]:
            # possible mirror found
            left = reversed(input[:i])
            right = input[i:]
            if all(map(lambda t: t[0] == t[1], zip(left, right))):
                return i

    return None
