from unittest import TestCase
from .part2 import parser


class Day07(TestCase):
    input = """
        32T3K 765
        T55J5 684
        KK677 28
        KTJJT 220
        QQQJA 483"""

    def test_day07_part2(self):
        game = parser.parse(self.input)
        self.assertEqual(5905, game.part2())
