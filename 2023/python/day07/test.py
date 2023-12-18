from unittest import TestCase
from . import parser, Game, Hand, Card


class Day07(TestCase):
    input = """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483"""

    def test_day07_parse(self):
        got = parser.parse(self.input)
        expected = Game(
            [
                Hand([Card(c) for c in list("32T3K")], 765),
                Hand([Card(c) for c in list("T55J5")], 684),
                Hand([Card(c) for c in list("KK677")], 28),
                Hand([Card(c) for c in list("KTJJT")], 220),
                Hand([Card(c) for c in list("QQQJA")], 483),
            ]
        )
        self.assertEqual(expected, got)
