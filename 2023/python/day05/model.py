import sys
from dataclasses import dataclass, field
from typing import List
from functools import reduce


@dataclass(frozen=True, slots=True)
class Range:
    dst: int = 0
    src: int = 0
    len: int = 0

    def dest(self, s: int) -> int | None:
        diff = s - self.src
        if 0 <= diff < self.len:
            return self.dst + diff
        return None


@dataclass(frozen=True, slots=True)
class RangeMap:
    name: str = field()
    ranges: List[Range] = field(default_factory=list)

    def dest(self, s: int) -> int:
        for r in self.ranges:
            if d := r.dest(s):
                return d
        return s


@dataclass(frozen=True, slots=True)
class Almanac:
    seeds: List[int] = field(default_factory=list)
    rangemaps: List[RangeMap] = field(default_factory=list)

    def min_location(self) -> int:
        result = []
        for s in self.seeds:
            result.append(reduce(lambda v, rm: rm.dest(v), self.rangemaps, s))
        return min(result)
