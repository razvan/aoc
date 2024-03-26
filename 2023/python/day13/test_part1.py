from unittest import TestCase
from .part1 import transpose, lines_before_mirror


class Part1(TestCase):
    def test_transpose(self):
        input = [
            "#.##..##.",
            "..#.##.#.",
            "##......#",
            "##......#",
            "..#.##.#.",
            "..##..##.",
            "#.#.##.#.",
        ]

        expected = [
            "#.##..#",
            "..##...",
            "##..###",
            "#....#.",
            ".#..#.#",
            ".#..#.#",
            "#....#.",
            "##..###",
            "..##...",
        ]

        actual = transpose(input)
        self.assertEqual(expected, actual)

    def test_lines_before_mirror_1(self):
        input = [
            "#.##..##.",
            "..#.##.#.",
            "##......#",
            "##......#",
            "..#.##.#.",
            "..##..##.",
            "#.#.##.#.",
        ]

        self.assertEqual(5, lines_before_mirror(input))

    def test_lines_before_mirror_2(self):
        input = [
            "#...##..#",
            "#....#..#",
            "..##..###",
            "#####.##.",
            "#####.##.",
            "..##..###",
            "#....#..#",
        ]

        self.assertEqual(400, lines_before_mirror(input))

    def test_lines_before_mirror_3(self):
        input = [
            "..#.....##.",
            ".#..#..##.#",
            ".......###.",
            "####.##.#.#",
            "###.###....",
            "###.###....",
            "####.##.#.#",
            ".......####",
            ".#..#..##.#",
            "..#.....##.",
            "..#.....##.",
            ".#..#..##.#",
            ".......####",
        ]
        self.assertEqual(1000, lines_before_mirror(input))
