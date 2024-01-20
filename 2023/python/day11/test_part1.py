from unittest import TestCase

from .part1 import (
    Puzzle,
    parser,
    solve,
    _transpose,
    _duplicate,
    _expand,
    _galaxies,
    _dist,
)


class Part1(TestCase):
    def test_day11_part1_solve(self):
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
        self.assertEqual(374, solve(puzzle))

    def test_day11_part1_transpose(self):
        self.assertEqual(["14", "25", "36"], list(_transpose(["123", "456"])))

    def test_day11_part1_duplicate(self):
        self.assertEqual(
            ["123", "...", "...", "456", "...", "..."],
            list(_duplicate(["123", "...", "456", "..."])),
        )

    def test_day11_part1_expand(self):
        self.assertEqual(
            ["1..2.3", "......", "......", "4..576", "......", "......"],
            list(_expand(["1.2.3", ".....", "4.576", "....."])),
        )

    def test_day11_part1_galaxies(self):
        input = [
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
        self.assertEqual(
            [
                (0, 4),
                (1, 9),
                (2, 0),
                (5, 8),
                (6, 1),
                (7, 12),
                (10, 9),
                (11, 0),
                (11, 5),
            ],
            list(_galaxies(_expand(input))),
        )

    def test_day11_part1_dist(self):
        self.assertEqual(
            [9, 15, 17, 5],
            list(
                _dist(
                    [
                        ((6, 1), (11, 5)),
                        ((0, 4), (10, 9)),
                        ((2, 0), (7, 12)),
                        ((11, 0), (11, 5)),
                    ]
                )
            ),
        )

    def test_day11_part1_parse(self):
        input = """
            ...#......
            .......#..
            #.........
            ..........
            ......#...
            .#........
            .........#
            ..........
            .......#..
            #...#.....
        """
        self.assertEqual(
            Puzzle(
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
            ),
            parser.parse(input),
        )
