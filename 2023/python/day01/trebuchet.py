"""
https://adventofcode.com/2023/day/1
"""
from typing import List, Tuple


def trebuchet(input: str):
    result = 0
    for line in input.splitlines():
        digits: List[str] = list(filter(lambda c: c.isdigit(), line))

        if len(digits) > 0:
            fl: Tuple[int, int] = (int(digits[0]), int(digits[-1]))

            result += int(f"{fl[0]}{fl[1]}")

    return result
