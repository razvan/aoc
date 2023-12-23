from dataclasses import dataclass
from typing import Dict, List, Set, Optional

from parsy import generate, regex, success, eof, string


class Day10Error(Exception):
    pass


TILE_CONN: Dict[str, List[str]] = {
    "|": ["N", "S"],
    "-": ["E", "W"],
    "L": ["N", "E"],
    "J": ["N", "W"],
    "7": ["S", "W"],
    "F": ["S", "E"],
    ".": [],
    "S": ["N", "S", "W", "E"],
}


@dataclass(frozen=True, slots=True)
class Loc:
    x: int
    y: int


@dataclass(frozen=True, slots=True)
class Puzzle:
    tiles: List[str]
    start: Loc
    width: int
    height: int


def peek_tile(
    dir: str, curr: Loc, p: Puzzle, seen: Set[Loc], prev: Optional[Loc] = None
) -> Optional[Loc]:
    match dir:
        case "N":
            # check north
            if curr.x - 1 >= 0:
                north = Loc(curr.x - 1, curr.y)
                if north not in seen and north != prev:
                    if "S" in TILE_CONN[p.tiles[north.x][north.y]]:
                        seen.add(north)
                        return north
        case "S":
            # check south
            if curr.x + 1 < p.height:
                south = Loc(curr.x + 1, curr.y)
                if south not in seen and south != prev:
                    if "N" in TILE_CONN[p.tiles[south.x][south.y]]:
                        seen.add(south)
                        return south
        case "W":
            # check west
            if curr.y - 1 >= 0:
                west = Loc(curr.x, curr.y - 1)
                if west not in seen and west != prev:
                    if "E" in TILE_CONN[p.tiles[west.x][west.y]]:
                        seen.add(west)
                        return west
        case "E":
            # check east
            if curr.y + 1 < p.width:
                east = Loc(curr.x, curr.y + 1)
                if east not in seen and east != prev:
                    if "W" in TILE_CONN[p.tiles[east.x][east.y]]:
                        seen.add(east)
                        return east
    return None


def next_tile(
    curr: Loc, p: Puzzle, seen: Set[Loc], prev: Optional[Loc] = None
) -> Optional[Loc]:
    """Find the next tile has not been [seen] yet and is not the [prev] tile
    (the one before the [curr] tile).
    The check for previous is needed to avoid a tile in the immediate
    vicinity of the [start] location returning [start] as the next tile at
    the beginning of the search.
    This can happen because the [start] location is never added to the [seen]
    set."""
    tile = p.tiles[curr.x][curr.y]
    for dir in TILE_CONN[tile]:
        if loc := peek_tile(dir, curr, p, seen, prev):
            return loc
    return None


def find_loop(p: Puzzle) -> List[Loc]:
    res: List[Loc] = [p.start]
    seen: Set[Loc] = set()
    while lres := len(res):
        prev: Optional[Loc] = res[-2] if lres > 1 else None
        next = next_tile(res[-1], p, seen, prev)
        if next == p.start:
            # found the loop
            return res
        elif next is None:
            # backtrack
            res.pop()
        else:
            res.append(next)

    raise Day10Error("Failed to find a loop starting at {}".format(p.start))


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day 10: part 1 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    return len(find_loop(puzzle)) // 2


@generate
def parser():
    pipe = regex(r"[.SFJ7L|-]+")
    newline = string("\n")
    padding = regex(r"\s*")
    tiles: List[str] = []
    start = None
    while True:
        line = yield (padding >> pipe << newline) | success(None)
        if not line:
            break
        if not start:
            try:
                start = Loc(len(tiles), line.index("S"))
            except ValueError:
                pass
        tiles.append(line)
        yield padding | eof
    if not start:
        raise Day10Error("Couldn't find the start location")
    return Puzzle(tiles, start, len(tiles[0]), len(tiles))
