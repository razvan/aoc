from .part2 import Puzzle, solve, parser
from unittest import TestCase


class Part2(TestCase):
    def test_day08_part2_puzzle(self):
        input = """
        LR

        11A = (11B, XXX)
        11B = (XXX, 11Z)
        11Z = (11B, XXX)
        22A = (22B, XXX)
        22B = (22C, 22C)
        22C = (22Z, 22Z)
        22Z = (22B, 22B)
        XXX = (XXX, XXX)
        """
        p: Puzzle = parser.parse(input)

        self.assertEqual(6, solve(p))
