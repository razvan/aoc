from collections import Counter
from dataclasses import dataclass, field
from enum import IntEnum
from typing import List, Self

from parsy import eof, generate, regex, success, whitespace


class Day07Error(Exception):
    pass


class Card(IntEnum):
    JOKER = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
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
        self._type = self._compute_type()

    def _compute_type(self) -> HandType:
        jokers = sum((1 for c in self.cards if c == Card.JOKER))
        counter = Counter((c for c in self.cards if c != Card.JOKER))
        counts = "".join([str(t[1]) for t in counter.most_common()])
        match jokers:
            case 0:
                match counts:
                    case "11111":
                        return HandType.HighCard
                    case "2111":
                        return HandType.OnePair
                    case "221":
                        return HandType.TwoPairs
                    case "311":
                        return HandType.ThreeOfAKind
                    case "32":
                        return HandType.FullHouse
                    case "41":
                        return HandType.FourOfAKind
                    case "5":
                        return HandType.FiveOfAKind
                    case _:
                        raise Day07Error(
                            f"Didn't expect counts {counts} for jokers {jokers}"
                        )
            case 1:
                match counts:
                    case "1111":
                        return HandType.OnePair
                    case "211":
                        return HandType.ThreeOfAKind
                    case "31":
                        return HandType.FourOfAKind
                    case "4":
                        return HandType.FiveOfAKind
                    case "22":
                        return HandType.FullHouse
                    case _:
                        raise Day07Error(
                            f"Didn't expect counts {counts} for jokers {jokers}"
                        )
            case 2:
                match counts:
                    case "111":
                        return HandType.ThreeOfAKind
                    case "21":
                        return HandType.FourOfAKind
                    case "3":
                        return HandType.FiveOfAKind
                    case _:
                        raise Day07Error(
                            f"Didn't expect counts {counts} for jokers {jokers}"
                        )
            case 3:
                match counts:
                    case "11":
                        return HandType.FourOfAKind
                    case "2":
                        return HandType.FiveOfAKind
                    case _:
                        raise Day07Error(
                            f"Didn't expect counts {counts} for jokers {jokers}"
                        )
            case 4 | 5:
                return HandType.FiveOfAKind
            case _:
                raise Day07Error(f"Didn't expect more than 5 jokers [{jokers}]")

    def __lt__(self, other: Self) -> bool:
        if self._type == other._type:
            return self.cards < other.cards
        else:
            return self._type < other._type


@dataclass(frozen=True, slots=True)
class Game:
    hands: List[Hand]

    def part2(self) -> int:
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
