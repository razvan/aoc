from dataclasses import dataclass, field
from parsy import eof, generate, regex, string, whitespace
from typing import List, Tuple, Iterable
from math import prod


@dataclass(frozen=True, slots=True)
class Race:
    time: int
    dist: int

    def options(self) -> Iterable[Tuple[int, int]]:
        return [(hold, hold * (self.time - hold)) for hold in range(self.time + 1)]

    def count_winning(self) -> int:
        return len([o for o in self.options() if o[1] > self.dist])


@dataclass(frozen=True, slots=True)
class Event:
    races: List[Race] = field(default_factory=list)

    def part1(self) -> int:
        return prod([r.count_winning() for r in self.races])

    def part2(self) -> int:
        return sum([r.count_winning() for r in self.races])


@generate
def parser():
    _num = regex(r"\d+").map(int)
    _pad = regex(r"\s*")
    times = yield _pad >> string("Time:") >> whitespace >> _num.sep_by(whitespace)
    dist = yield _pad >> string("Distance:") >> whitespace >> _num.sep_by(whitespace)
    yield _pad | eof
    return Event([Race(t, d) for t, d in zip(times, dist)])


def main(f: List[str]):
    with open(f[0]) as input:
        strin = input.read()
        print("Day 06: part 1 is {}".format(parser.parse(strin).part1()))
    with open(f[1]) as input:
        strin = input.read()
        print("Day 06: part 2 is {}".format(parser.parse(strin).part2()))
