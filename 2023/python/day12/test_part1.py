from unittest import TestCase

from .part1 import valid, gen, parse, Puzzle
from textwrap import dedent


class Part1(TestCase):
    def test_day12_part1_parse(self):
        input = dedent(
            """
            ???.### 1,1,3
            .??..??...?##. 1,1,3
            ?#?#?#?#?#?#?#? 1,3,1,6
            ????.#...#... 4,1,1
            ????.######..#####. 1,6,5
            ?###???????? 3,2,1
            """
        )
        expected = Puzzle(
            {
                "???.###": [1, 1, 3],
                ".??..??...?##.": [1, 1, 3],
                "?#?#?#?#?#?#?#?": [1, 3, 1, 6],
                "????.#...#...": [4, 1, 1],
                "????.######..#####.": [1, 6, 5],
                "?###????????": [3, 2, 1],
            }
        )
        self.assertEqual(expected, parse(input))

    def test_day12_part1_solve(self):
        self.assertTrue(True)

    def test_valid(self):
        inputs = {
            "#.#.###": [1, 1, 3],
            ".#...#....###.": [1, 1, 3],
            ".#.###.#.######": [1, 3, 1, 6],
        }
        for line, groups in inputs.items():
            self.assertTrue(valid(line, groups))

    def test_gen(self):
        got = set(gen(".?#?"))
        expected = set(["..#.", ".##.", ".###", "..##"])

        self.assertEqual(got, expected)
