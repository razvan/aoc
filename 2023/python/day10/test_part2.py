from unittest import TestCase

from .part2 import Puzzle, parser, solve, Tile, find_loop


class Part2(TestCase):
    def test_day10_part2_parse(self):
        input = """
        .F----7F7F7F7F-7....
        .|F--7||||||||FJ....
        .||.FJ||||||||L7....
        FJL7L7LJLJ||LJ.L-7..
        L--J.L7...LJS7F-7L7.
        ....F-J..F7FJ|L7L7L7
        ....L7.F7||L7|.L7L7|
        .....|FJLJ|FJ|F7|.LJ
        ....FJL-7.||.||||...
        ....L---J.LJ.LJLJ...
        """
        expected = Puzzle(
            tiles=[
                ".F----7F7F7F7F-7....",
                ".|F--7||||||||FJ....",
                ".||.FJ||||||||L7....",
                "FJL7L7LJLJ||LJ.L-7..",
                "L--J.L7...LJS7F-7L7.",
                "....F-J..F7FJ|L7L7L7",
                "....L7.F7||L7|.L7L7|",
                ".....|FJLJ|FJ|F7|.LJ",
                "....FJL-7.||.||||...",
                "....L---J.LJ.LJLJ...",
            ],
            start=Tile(4, 12, "S"),
            width=20,
            height=10,
        )
        self.assertEqual(expected, parser.parse(input))

    def test_day10_part2_iter(self):
        puzzle = Puzzle(
            tiles=[
                ".F----7F7F7F7F-7....",
            ],
            start=Tile(4, 12, "S"),
            width=20,
            height=10,
        )
        it = iter(puzzle)
        self.assertEqual(Tile(0, 0, "."), next(it))
        self.assertEqual(Tile(0, 1, "F"), next(it))
        self.assertEqual(Tile(0, 2, "-"), next(it))

    def test_day10_part2_solve(self):
        puzzle = Puzzle(
            tiles=[
                ".F----7F7F7F7F-7....",
                ".|F--7||||||||FJ....",
                ".||.FJ||||||||L7....",
                "FJL7L7LJLJ||LJ.L-7..",
                "L--J.L7...LJS7F-7L7.",
                "....F-J..F7FJ|L7L7L7",
                "....L7.F7||L7|.L7L7|",
                ".....|FJLJ|FJ|F7|.LJ",
                "....FJL-7.||.||||...",
                "....L---J.LJ.LJLJ...",
            ],
            start=Tile(4, 12, "S"),
            width=20,
            height=10,
        )
        self.assertEqual(8, solve(puzzle))

    def test_day10_part2_solve2(self):
        puzzle = Puzzle(
            tiles=[
                "FF7FSF7F7F7F7F7F---7",
                "L|LJ||||||||||||F--J",
                "FL-7LJLJ||||||LJL-77",
                "F--JF--7||LJLJ7F7FJ-",
                "L---JF-JLJ.||-FJLJJ7",
                "|F|F-JF---7F7-L7L|7|",
                "|FFJF7L7F-JF7|JL---7",
                "7-L-JL7||F7|L7F-7F7|",
                "L.L7LFJ|||||FJL7||LJ",
                "L7JLJL-JLJLJL--JLJ.L",
            ],
            start=Tile(0, 4, "S"),
            width=20,
            height=10,
        )
        self.assertEqual(10, solve(puzzle))

    def test_day10_part2_solve3(self):
        puzzle = Puzzle(
            tiles=["..F7.", ".FJ|.", "SJ.L7", "|F--J", "LJ..."],
            start=Tile(2, 0, "S"),
            width=5,
            height=5,
        )
        self.assertEqual(1, solve(puzzle))

    def test_day10_part2_find_loop(self):
        p = Puzzle(
            tiles=["..F7.", ".FJ|.", "SJ.L7", "|F--J", "LJ..."],
            start=Tile(2, 0, "S"),
            width=5,
            height=5,
        )
        expected = [
            Tile(x=2, y=0),
            Tile(x=3, y=0),
            Tile(x=4, y=0),
            Tile(x=4, y=1),
            Tile(x=3, y=1),
            Tile(x=3, y=2),
            Tile(x=3, y=3),
            Tile(x=3, y=4),
            Tile(x=2, y=4),
            Tile(x=2, y=3),
            Tile(x=1, y=3),
            Tile(x=0, y=3),
            Tile(x=0, y=2),
            Tile(x=1, y=2),
            Tile(x=1, y=1),
            Tile(x=2, y=1),
        ]
        self.assertEqual(expected, find_loop(p))

    def test_day10_part2_sorted(self):
        path = [
            Tile(x=4, y=0),
            Tile(x=4, y=1),
            Tile(x=2, y=0),
            Tile(x=3, y=0),
        ]
        expected = [
            Tile(x=2, y=0),
            Tile(x=3, y=0),
            Tile(x=4, y=0),
            Tile(x=4, y=1),
        ]
        self.assertEqual(expected, sorted(path))

    def test_day10_part2_intersect(self):
        s1 = [
            Tile(x=4, y=2, tile="|"),
            Tile(x=4, y=1, tile="|"),
            Tile(x=2, y=0, tile="|"),
            Tile(x=3, y=2, tile="|"),
        ]
        s2 = [
            Tile(x=4, y=0, tile="-"),
            Tile(x=4, y=1, tile="-"),
            Tile(x=2, y=0, tile="-"),
            Tile(x=3, y=0, tile="-"),
        ]
        expected = set(
            [
                Tile(x=4, y=1, tile="|"),
                Tile(x=2, y=0, tile="-"),
            ]
        )
        self.assertEqual(expected, set(s1).intersection(s2))
