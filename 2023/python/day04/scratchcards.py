from dataclasses import dataclass, field
from parsy import eof, string, regex, seq
from typing import List
import sys


@dataclass(frozen=True, slots=True)
class Card:
    id: int = field(default=0)
    winning: List[int] = field(default_factory=list)
    owning: List[int] = field(default_factory=list)

    def points(self) -> int:
        matching: int = len(set(self.winning).intersection(set(self.owning)))
        if matching < 2:
            return matching
        else:
            return 2 ** (matching - 1)


@dataclass(frozen=True, slots=True)
class Scratchcards:
    cards: List[Card] = field(default_factory=list)

    def points(self) -> int:
        return sum(map(lambda c: c.points(), self.cards))


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


if __name__ == "__main__":
    main(sys.argv[1])
