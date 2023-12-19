from .part1 import Puzzle, solve, parser
from unittest import TestCase


class Part1(TestCase):
    def test_day08_puzzle(self):
        p = Puzzle(
            "LLR",
            "AAA",
            {"AAA": ("BBB", "BBB"), "BBB": ("AAA", "ZZZ"), "ZZZ": ("ZZZ", "ZZZ")},
        )
        self.assertEqual(6, solve(p))

    def test_day08_parser(self):
        input = """
        LLR

        AAA = (BBB, BBB)
        BBB = (AAA, ZZZ)
        ZZZ = (ZZZ, ZZZ)
        """
        got = parser.parse(input)
        expected = Puzzle(
            "LLR",
            "AAA",
            {"AAA": ("BBB", "BBB"), "BBB": ("AAA", "ZZZ"), "ZZZ": ("ZZZ", "ZZZ")},
        )
        self.assertEqual(expected, got)
