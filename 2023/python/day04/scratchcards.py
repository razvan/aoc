import sys
from array import array
from dataclasses import dataclass, field
from functools import cached_property
from typing import List

from parsy import eof, regex, seq, string


@dataclass(frozen=True)
class Card:
    id: int = field(default=0)
    winning: List[int] = field(default_factory=list)
    owning: List[int] = field(default_factory=list)

    @cached_property
    def matching(self):
        return len(set(self.winning).intersection(set(self.owning)))

    def points(self) -> int:
        if self.matching < 2:
            return self.matching
        else:
            return 2 ** (self.matching - 1)


@dataclass(frozen=True, slots=True)
class Scratchcards:
    cards: List[Card] = field(default_factory=list)

    def points(self) -> int:
        return sum(map(lambda c: c.points(), self.cards))

    def winning_cards(self) -> int:
        len_cards = len(self.cards)
        seen_cards = array("L", [1 for _ in range(len_cards)])

        for i, c in enumerate(self.cards):
            # print(seen_cards)
            copies = seen_cards[i]
            _from = min(len_cards, i + 1)
            _to = min(len_cards, i + c.matching + 1)
            seen_cards[_from:_to] = array(
                "L", [x + copies for x in seen_cards[_from:_to]]
            )

        return sum(seen_cards)


str_card = string("Card")
num = regex(r"\d+")
opt_whitespace = regex(r"\s*")
whitespace = regex(r"\s+")
colon = string(":")
bar = string("|")

card = seq(
    _p1=opt_whitespace >> str_card >> whitespace,
    id=num.map(int),
    _p2=colon >> whitespace,
    winning=num.map(int).sep_by(whitespace),
    _p3=whitespace >> bar >> whitespace,
    owning=num.map(int).sep_by(whitespace),
    _p4=opt_whitespace | eof,
).combine_dict(Card)

scratchcards = card.many().combine(lambda *c: Scratchcards(cards=c))


def parse(input: str) -> Scratchcards:
    return scratchcards.parse(input)


def main(f: str):
    with open(f) as input:
        strin = input.read()
        scratchcards = parse(strin)
        print("Day 04: scratchcards points {}".format(scratchcards.points()))
        print("Day 04: winning scratchcards {}".format(scratchcards.winning_cards()))


if __name__ == "__main__":
    main(sys.argv[1])
