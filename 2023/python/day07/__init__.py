from dataclasses import dataclass, field, fields
from parsy import eof, generate, regex, success, whitespace
from typing import List, Tuple, Iterable
from math import prod
from enum import StrEnum
from pprint import pprint


class Card(StrEnum):
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "T"
    JOKER = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


@dataclass(frozen=True, slots=True)
class Hand:
    cards: List[Card]
    bid: int


@dataclass(frozen=True, slots=True)
class Game:
    hands: List[Hand]

    def part1(self):
        pass


@generate
def parser():
    _num = regex(r"\d+").map(int)
    _pad = regex(r"\s*")
    _cards = regex(r"[23456789TJQKA]{5}").desc("valid cards")
    hands: List[Hand] = []
    while True:
        cards = yield (_pad >> _cards << whitespace) | success(None)
        if not cards:
            break
        else:
            bid = yield _num << _pad
            hands.append(Hand([Card(c) for c in cards], bid))
    yield _pad | eof
    return Game(hands)


def main(f: List[str]):
    with open(f[0]) as input:
        strin = input.read()
        # print("Day 07: part 1 is {}".format(parser.parse(strin).part1()))
        pprint(parser.parse(strin))
