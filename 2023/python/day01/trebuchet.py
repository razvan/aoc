"""
https://adventofcode.com/2023/day/1
"""
from typing import List, Optional, Tuple


def trebuchet(input: str):
    calibration_values: List[int] = []
    for line in input.splitlines():
        digits: List[str] = list(filter(lambda c: c.isdigit(), line))

        fl: Tuple[Optional[int], Optional[int]] = (None, None)

        if len(digits) > 1:
            fl = (int(digits[0]), int(digits[-1]))
        if len(digits) == 1:
            fl = (int(digits[0]), int(digits[0]))

        if fl[0] is not None:
            calibration_values.append(int(f"{fl[0]}{fl[1]}"))
    return sum(calibration_values)
