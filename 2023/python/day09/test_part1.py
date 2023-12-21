from unittest import TestCase

from .part1 import Puzzle, parser, solve, predict


class Part1(TestCase):
    def test_day09_parse(self):
        input = """
            0 3 6 9 12 15
            1 3 6 10 15 21
            10 13 16 21 30 45
        """
        expected = Puzzle(
            [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
        )
        got = parser.parse(input)
        self.assertEqual(expected, got)

    def test_day09_solve(self):
        p = Puzzle(
            [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
        )

        self.assertEqual(114, solve(p))

    def test_day09_predict(self):
        input = [10, 13, 16, 21, 30, 45]
        self.assertEqual(68, predict(input))
