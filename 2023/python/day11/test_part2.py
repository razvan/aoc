from itertools import combinations
from unittest import TestCase

from .part2 import (
    Puzzle,
    ScaleRange,
    _dist,
    _expand,
    _galaxies,
    _scale_ranges,
    _transpose,
    _scale,
)


class Part2(TestCase):
    def test_day11_part2_expand10(self):
        puzzle = Puzzle(
            [
                "...#......",
                ".......#..",
                "#.........",
                "..........",
                "......#...",
                ".#........",
                ".........#",
                "..........",
                ".......#..",
                "#...#.....",
            ]
        )
        scale_ranges = _expand(puzzle.input, 10)
        got = sum(_dist(combinations(_galaxies(puzzle.input, *scale_ranges), 2)))
        self.assertEqual(1030, got)

    def test_day11_part2_expand100(self):
        puzzle = Puzzle(
            [
                "...#......",
                ".......#..",
                "#.........",
                "..........",
                "......#...",
                ".#........",
                ".........#",
                "..........",
                ".......#..",
                "#...#.....",
            ]
        )
        scale_ranges = _expand(puzzle.input, 100)
        got = sum(_dist(combinations(_galaxies(puzzle.input, *scale_ranges), 2)))
        self.assertEqual(8410, got)

    def test_day11_part2_scale_ranges_rows(self):
        puzzle = Puzzle(
            [
                "...#......",
                ".......#..",
                "#.........",
                "..........",
                "......#...",
                ".#........",
                ".........#",
                "..........",
                ".......#..",
                "#...#.....",
            ]
        )
        scale_ranges = _scale_ranges(puzzle.input, 2)
        self.assertEqual(
            [
                ScaleRange(3, 2),
                ScaleRange(7, 2 * 2),
            ],
            scale_ranges,
        )

    def test_day11_part2_scale_ranges_cols(self):
        puzzle = Puzzle(
            [
                "...#......",
                ".......#..",
                "#.........",
                "..........",
                "......#...",
                ".#........",
                ".........#",
                "..........",
                ".......#..",
                "#...#.....",
            ]
        )
        scale_ranges = _scale_ranges(_transpose(puzzle.input), 2)
        self.assertEqual(
            [
                ScaleRange(2, 2 * 1),
                ScaleRange(5, 2 * 2),
                ScaleRange(8, 2 * 3),
            ],
            scale_ranges,
        )

    def test_day11_part2_scale(self):
        scale_ranges = [
            ScaleRange(3, 1),
            ScaleRange(7, 1 * 2),
        ]
        self.assertEqual([5, 10], [_scale(i, scale_ranges) for i in [4, 8]])
