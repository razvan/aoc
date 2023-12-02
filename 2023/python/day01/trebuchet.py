"""
https://adventofcode.com/2023/day/1
"""
import textwrap
from typing import List


def trebuchet(input: str):
    calibration_values: List[int] = []
    for line in input.splitlines():
        digits: List[str] = list(filter(lambda c: c.isdigit(), line))
        if len(digits) > 1:
            calibration_values.append(int(f"{digits[0]}{digits[-1]}"))
        if len(digits) == 1:
            calibration_values.append(int(f"{digits[0]}{digits[0]}"))
    return sum(calibration_values)


if __name__ == "__main__":
    input: str = textwrap.dedent(
        """
        1abc2
        pqr3stu8vwx
        a1b2c3d4e5f
        treb7uchet
        """
    )

    print(trebuchet(input))
