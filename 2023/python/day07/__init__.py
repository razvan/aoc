from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Self, Tuple

from parsy import eof, generate, regex, success, whitespace


class Day07Error(Exception):
    pass


class Card(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JOKER = 11
    QUEEN = 12
    KING = 13
    ACE = 14


def card_from(c: str) -> Card:
    if c.isnumeric():
        v = int(c)
        if 1 < v < 10:
            return Card(v)
        else:
            raise Day07Error(f"Invalid card value {c}")
    elif c == "T":
        return Card.TEN
    elif c == "J":
        return Card.JOKER
    elif c == "Q":
        return Card.QUEEN
    elif c == "K":
        return Card.KING
    elif c == "A":
        return Card.ACE
    raise Day07Error(f"Invalid card value {c}")


class HandType(IntEnum):
    HighCard = 0
    OnePair = 1
    TwoPairs = 2
    ThreeOfAKind = 3
    FullHouse = 4
    FourOfAKind = 5
    FiveOfAKind = 6


@dataclass(slots=True)
class Hand:
    cards: List[Card] = field(default_factory=list)
    bid: int = field(default=0)

    _type: HandType = field(init=False)

    def __post_init__(self):
        """Compute the hand type"""
        mc = Counter(self.cards).most_common()
        if len(mc) == 5:
            self._type = HandType.HighCard
        elif len(mc) == 4:
            self._type = HandType.OnePair
        elif len(mc) == 3:
            if mc[0][1] == 3:
                self._type = HandType.ThreeOfAKind
            else:
                self._type = HandType.TwoPairs
        elif len(mc) == 2:
            if mc[0][1] == 3:
                self._type = HandType.FullHouse
            else:
                self._type = HandType.FourOfAKind
        elif len(mc) == 1:
            self._type = HandType.FiveOfAKind

    def __lt__(self, other: Self) -> bool:
        if self._type == other._type:
            return self.cards < other.cards
        else:
            return self._type < other._type


@dataclass(frozen=True, slots=True)
class Game:
    hands: List[Hand]

    def part1(self) -> int:
        return sum(
            (hand.bid * (rank + 1) for rank, hand in enumerate(sorted(self.hands)))
        )


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
            hands.append(Hand([card_from(c) for c in cards], bid))
    yield _pad | eof
    return Game(hands)


def main(f: List[str]):
    with open(f[0]) as input:
        strin = input.read()
        game = parser.parse(strin)
        print("Day 07: part 1 is {}".format(game.part1()))
