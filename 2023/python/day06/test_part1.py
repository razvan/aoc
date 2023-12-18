from unittest import TestCase
from . import Event, Race, parser


class Day06(TestCase):
    input = """
        Time:      7  15   30
        Distance:  9  40  200"""

    def test_day06_event_parse(self):
        got = parser.parse(self.input)
        expected = Event([Race(7, 9), Race(15, 40), Race(30, 200)])
        self.assertEqual(expected, got)

    def test_day06_race_moves(self):
        ev = parser.parse(self.input)
        got = ev.races[0].options()
        expected = [(0, 0), (1, 6), (2, 10), (3, 12), (4, 12), (5, 10), (6, 6), (7, 0)]
        self.assertEqual(expected, got)

    def test_day06_count_winning(self):
        ev = parser.parse(self.input)
        got = ev.races[0].count_winning()
        self.assertEqual(4, got)

    def test_day06_event_count_winning(self):
        ev = parser.parse(self.input)
        got = ev.part1()
        self.assertEqual(288, got)

    def test_day06_part_two(self):
        input = """
        Time:      71530
        Distance:  940200
        """
        ev = parser.parse(input)
        got = ev.part2()
        self.assertEqual(71503, got)
