from unittest import TestCase

from .part1 import Puzzle, find_loop, parser, peek_tile, solve, Loc, next_tile


class Part1(TestCase):
    def test_day10_part1_parse(self):
        input = """
        ..F7.
        .FJ|.
        SJ.L7
        |F--J
        LJ...
        """
        #  01234 <- y
        # 0..F7.
        # 1.FJ|.
        # 2SJ.L7
        # 3|F--J
        # 4LJ...
        # ^
        # |
        # x
        expected = Puzzle(
            tiles=["..F7.", ".FJ|.", "SJ.L7", "|F--J", "LJ..."],
            start=Loc(2, 0),
            width=5,
            height=5,
        )
        self.assertEqual(expected, parser.parse(input))

    def test_day10_part1_solve(self):
        p = Puzzle(
            tiles=["..F7.", ".FJ|.", "SJ.L7", "|F--J", "LJ..."],
            start=Loc(2, 0),
            width=5,
            height=5,
        )
        self.assertEqual(8, solve(p))

    def test_day10_peek_tile(self):
        p = Puzzle(
            tiles=["..F7.", ".FJ|.", "SJ.L7", "|F--J", "LJ..."],
            start=Loc(2, 0),
            width=5,
            height=5,
        )

        self.assertEqual(None, peek_tile("N", p.start, p, set()))
        self.assertEqual(Loc(3, 0), peek_tile("S", p.start, p, set()))
        self.assertEqual(Loc(2, 1), peek_tile("E", p.start, p, set()))
        self.assertEqual(None, peek_tile("W", p.start, p, set()))

    def test_day10_next_tile(self):
        p = Puzzle(
            tiles=["..F7.", ".FJ|.", "SJ.L7", "|F--J", "LJ..."],
            start=Loc(2, 0),
            width=5,
            height=5,
        )
        seen = set()
        self.assertEqual(Loc(3, 0), next_tile(p.start, p, seen))
        self.assertEqual(Loc(2, 1), next_tile(p.start, p, seen))
        self.assertEqual(None, next_tile(p.start, p, seen))
        self.assertEqual(None, next_tile(p.start, p, seen))

    def test_day10_find_loop(self):
        p = Puzzle(
            tiles=["..F7.", ".FJ|.", "SJ.L7", "|F--J", "LJ..."],
            start=Loc(2, 0),
            width=5,
            height=5,
        )
        expected = [
            Loc(x=2, y=0),
            Loc(x=3, y=0),
            Loc(x=4, y=0),
            Loc(x=4, y=1),
            Loc(x=3, y=1),
            Loc(x=3, y=2),
            Loc(x=3, y=3),
            Loc(x=3, y=4),
            Loc(x=2, y=4),
            Loc(x=2, y=3),
            Loc(x=1, y=3),
            Loc(x=0, y=3),
            Loc(x=0, y=2),
            Loc(x=1, y=2),
            Loc(x=1, y=1),
            Loc(x=2, y=1),
        ]
        self.assertEqual(expected, find_loop(p))
