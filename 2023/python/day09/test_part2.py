from unittest import TestCase

from .part2 import Puzzle, solve, predict


class Part2(TestCase):
    def test_day09_part2_predict(self):
        # self.assertEqual(5, predict([10, 13, 16, 21, 30, 45]))
        self.assertEqual(0, predict([1, 3, 6, 10, 15, 21]))
        # 0 1 3 6 10 15 21
        # 1 2 3 4 5 6
        # 1 1 1 1 1
        # 0 0 0 0

    def test_day09_part2_solve(self):
        p = Puzzle(
            [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]
        )
        self.assertEqual(2, solve(p))  # -3, 0, 5
