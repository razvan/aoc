from typing import List
from .part1 import run as run1
from .part2 import run as run2


def main(args: List[str]):
    run1(args[0])
    run2(args[0])


__all__ = ["main"]
