"""
https://adventofcode.com/2023/day/3
"""

import sys
from typing import List, Dict, Tuple, Set
from dataclasses import dataclass, field


def issymbol(s: str) -> bool:
    return not s.isnumeric() and s != "."


@dataclass
class EngineSchema:
    schema: Dict[Tuple[int, int], str] = field(default_factory=dict)
    rows: int = field(default=0)
    cols: int = field(default=0)

    def add(self, i: int, j: int, cell: str):
        self.schema[(i, j)] = cell
        self.rows = max(self.rows, i + 1)
        self.cols = max(self.cols, j + 1)

    def dim(self):
        return (self.rows, self.cols)

    def codes(self, rows=None, cols=None) -> List[Tuple[int, int, str]]:
        """Return a list of codes and their start location."""
        result: List[Tuple[int, int, str]] = []
        for i in range(rows if rows else self.rows):
            digits: List[Tuple[int, int, str]] = []
            for j in range(cols if cols else self.cols):
                cell: str = self.schema[(i, j)]
                if cell.isnumeric():
                    digits.append((i, j, cell))
                else:
                    if len(digits):
                        number = "".join(map(lambda t: t[2], digits))
                        result.append((digits[0][0], digits[0][1], number))
                    digits = []
            # check if a number was last in a row
            if len(digits):
                number = "".join(map(lambda t: t[2], digits))
                result.append((digits[0][0], digits[0][1], number))
            digits = []
        return result

    def is_symloc(self, i: int, j: int) -> bool:
        if i < 0 or i >= self.rows:
            return False
        if j < 0 or j >= self.cols:
            return False
        return issymbol(self.schema[(i, j)])

    def is_adjacent_sym(self, row: int, col: int, code_len: int) -> bool:
        # check previous row including the diagonals NW and NE
        for j in range(col - 1, col + code_len + 1):
            if self.is_symloc(row - 1, j):
                return True
        # check next row including the diagonals SW and SE
        for j in range(col - 1, col + code_len + 1):
            if self.is_symloc(row + 1, j):
                return True
        # check east and west
        if self.is_symloc(row, col - 1) or self.is_symloc(row, col + code_len):
            return True

        return False

    def part_numbers(self) -> List[int]:
        result: List[int] = []
        for i, j, snum in self.codes():
            if self.is_adjacent_sym(i, j, len(snum)):
                result.append(int(snum))
        return result

    def gear_numbers(self) -> List[Tuple[int, int]]:
        return []

    def __repr__(self) -> str:
        lines = []
        for i in range(self.rows):
            lines.append("".join([self.schema[(i, j)] for j in range(self.cols)]))
        return "\n".join(lines)


def parse_engine_schema(input: str) -> EngineSchema:
    result: EngineSchema = EngineSchema()

    # enumerate lines while skipping any empty lines.
    # empty lines are skipped in before the enumeration
    # (in the list comprehension) to keep the indices (i,j)
    # in order
    for i, line in enumerate([line for line in input.splitlines() if line]):
        for j, cell in enumerate(line):
            result.add(i, j, cell)

    return result


def engine_part(engine: str) -> int:
    return 0


def main(f: str):
    with open(f) as input:
        strin = input.read()
        e = parse_engine_schema(strin)
        print("Day 03: sum of the part numbers is {}".format(sum(e.part_numbers())))


if __name__ == "__main__":
    main(sys.argv[1])
