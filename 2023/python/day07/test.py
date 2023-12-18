from unittest import TestCase, expectedFailure
from . import parser, Game, Hand, Card, card_from
from pprint import pprint


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
                Hand([card_from(c) for c in list("32T3K")], 765),
                Hand([card_from(c) for c in list("T55J5")], 684),
                Hand([card_from(c) for c in list("KK677")], 28),
                Hand([card_from(c) for c in list("KTJJT")], 220),
                Hand([card_from(c) for c in list("QQQJA")], 483),
            ]
        )
        self.assertEqual(expected, got)

    def test_day07_sorted_hands(self):
        input = [
            Hand([card_from(c) for c in list("QQQJA")], 483),
            Hand([card_from(c) for c in list("T55J5")], 684),
            Hand([card_from(c) for c in list("KK677")], 28),
            Hand([card_from(c) for c in list("KTJJT")], 220),
            Hand([card_from(c) for c in list("32T3K")], 765),
        ]

        expected = [
            Hand([card_from(c) for c in list("32T3K")], 765),
            Hand([card_from(c) for c in list("KTJJT")], 220),
            Hand([card_from(c) for c in list("KK677")], 28),
            Hand([card_from(c) for c in list("T55J5")], 684),
            Hand([card_from(c) for c in list("QQQJA")], 483),
        ]
        self.assertEqual(expected, sorted(input))

    def test_day07_hand_types(self):
        game = Game(
            [
                Hand([card_from(c) for c in list("22336")], 2),
                Hand([card_from(c) for c in list("33226")], 1),
            ]
        )

        self.assertEqual(4, game.part1())

    def test_day07_test_from_reddit(self):
        input = """
            AAAAA 2
            22222 3
            AAAAK 5
            22223 7
            AAAKK 11
            22233 13
            AAAKQ 17
            22234 19
            AAKKQ 23
            22334 29
            AAKQJ 31
            22345 37
            AKQJT 41
            23456 43
         """
        game = parser.parse(input)
        self.assertEqual(1343, game.part1())

    def test_day07_part1(self):
        game = parser.parse(self.input)
        self.assertEqual(6440, game.part1())
