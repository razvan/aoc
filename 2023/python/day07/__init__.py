from .part1 import parser as part1_parser
from .part2 import parser as part2_parser
from typing import List


def main(f: List[str]):
    with open(f[0]) as input:
        strin = input.read()
        game = part1_parser.parse(strin)
        print("Day 07: part 1 is {}".format(game.part1()))
        game = part2_parser.parse(strin)
        print("Day 07: part 2 is {}".format(game.part2()))
