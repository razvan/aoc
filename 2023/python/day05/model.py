import sys
from dataclasses import dataclass, field
from typing import List, Iterable, Tuple
from functools import reduce
from itertools import pairwise
from pprint import pprint


@dataclass(frozen=True, slots=True)
class Segment:
    src: int
    len: int

    @property
    def end(self) -> int:
        return self.src + self.len


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

    @property
    def end(self):
        return self.src + self.len

    def merge(
        self, sgmts: Iterable[Segment]
    ) -> Tuple[Iterable[Segment], Iterable[Segment]]:
        mapped = []
        others = []
        for sgmt in sgmts:
            if sgmt.src < self.src:
                if sgmt.end < self.src:
                    others.append(sgmt)
                elif sgmt.end < self.end:
                    others.append(Segment(sgmt.src, self.src - sgmt.src))
                    mapped.append(Segment(self.dst, sgmt.end - self.src))
                else:
                    others.extend(
                        [
                            Segment(sgmt.src, self.src - sgmt.src),
                            Segment(self.end, sgmt.len - sgmt.end - self.end),
                        ]
                    )

                    mapped.append(Segment(self.dst, sgmt.end - self.src))
            elif sgmt.src < self.end:
                if sgmt.end < self.end:
                    mapped.append(Segment(self.dst, sgmt.len))
                else:
                    mapped.append(Segment(self.dst, self.end - sgmt.src))
                    others.append(Segment(self.end, sgmt.end - self.end))
            else:
                others.append(sgmt)

        return (others, mapped)


@dataclass(frozen=True, slots=True)
class RangeMap:
    name: str = field()
    ranges: List[Range] = field(default_factory=list)

    def dest(self, s: int) -> int:
        for r in self.ranges:
            if d := r.dest(s):
                return d
        return s

    def dest_segment(self, sgmts: Iterable[Segment]) -> Iterable[Segment]:
        res = []
        ir = iter(self.ranges)
        others, mapped = next(ir).merge(sgmts)
        res.extend(mapped)
        while True:
            try:
                others, mapped = next(ir).merge(others)
                res.extend(mapped)
            except StopIteration:
                break
        res.extend(others)
        return res


@dataclass(frozen=True, slots=True)
class Almanac:
    seeds: List[int] = field(default_factory=list)
    rangemaps: List[RangeMap] = field(default_factory=list)

    def min_location(self) -> int:
        result = []
        for s in self.seeds:
            result.append(reduce(lambda v, rm: rm.dest(v), self.rangemaps, s))
        return min(result)

    def min_location_seed_ranges(self) -> int:
        seed_ranges = [Segment(src, _len) for src, _len in pairwise(self.seeds)]
        result = reduce(lambda v, rm: rm.dest_segment(v), self.rangemaps, seed_ranges)
        # TODO: figure out where all the segments with src=0 are comming from.
        min = next(filter(lambda x: x.src > 0, sorted(result, key=lambda x: x.src)))
        # pprint(min)
        return min.src
