from parsy import generate, regex, string, success, eof, whitespace
from typing import List
from .model import Almanac, Range, RangeMap

_padding = regex(r"\s*")  # optional whitespace
_num = regex(r"\d+").map(int).desc("expected a number")

_s_seeds = string("seeds:")
_s_map_name = (
    string("seed-to-soil map:")
    | string("soil-to-fertilizer map:")
    | string("fertilizer-to-water map:")
    | string("water-to-light map:")
    | string("light-to-temperature map:")
    | string("temperature-to-humidity map:")
    | string("humidity-to-location map:")
)


@generate
def seeds():
    res: List[int] = []
    yield _padding >> _s_seeds >> whitespace
    res = yield _num.sep_by(whitespace)
    return res


@generate
def env_map():
    mname = yield _padding >> _s_map_name << _padding
    r: List[Range] = []
    while True:
        tpl = yield _num.sep_by(whitespace, min=3, max=3) | success(None)
        if tpl is None:
            break
        else:
            r.append(Range(*tpl))
        yield _padding | eof

    return RangeMap(mname, r)


@generate
def almanac():
    s = yield seeds
    rms = yield env_map.many()
    return Almanac(s, rms)
