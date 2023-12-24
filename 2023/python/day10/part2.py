from dataclasses import dataclass, field
from typing import (
    Dict,
    List,
    Set,
    Optional,
    Generator,
)

from parsy import generate, regex, success, eof, string


class Day10Error(Exception):
    pass


"""The connections a specific tile can have.

For example, the "|" can connect to the north (N) tile and the south (S) tile,
while the "L" tile cann connect to the north (N) tile and the east (E) tile.

The start tile (S) can connect in all directions and the ground (.) tile has
no connections at all.
"""
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


@dataclass(frozen=True, slots=True, order=True)
class Tile:
    x: int
    y: int
    tile: str = field(default=".", compare=False)


@dataclass(frozen=True, slots=True)
class Puzzle:
    tiles: List[str]
    start: Tile
    width: int
    height: int

    def __iter__(self) -> Generator[Tile, None, None]:
        for i, row in enumerate(self.tiles):
            for j, tile in enumerate(row):
                yield Tile(i, j, tile)


def peek_tile(
    dir: str, curr: Tile, p: Puzzle, seen: Set[Tile], prev: Optional[Tile] = None
) -> Optional[Tile]:
    """Return a tile that is connected to the [curr] tile in the [dir] direction
    and has not been seen yet.

    A tile has been seen if it's in the [seen] set or the [prev] tile.

    The returned tile is added to the [seen] set.

    Return None if no connecting tile is found.
    """
    match dir:
        case "N":
            # check north
            if curr.x - 1 >= 0:
                tile = p.tiles[curr.x - 1][curr.y]
                north = Tile(curr.x - 1, curr.y, tile)
                if north not in seen and north != prev:
                    if "S" in TILE_CONN[tile]:
                        seen.add(north)
                        return north
        case "S":
            # check south
            if curr.x + 1 < p.height:
                tile = p.tiles[curr.x + 1][curr.y]
                south = Tile(curr.x + 1, curr.y, tile)
                if south not in seen and south != prev:
                    if "N" in TILE_CONN[tile]:
                        seen.add(south)
                        return south
        case "W":
            # check west
            if curr.y - 1 >= 0:
                tile = p.tiles[curr.x][curr.y - 1]
                west = Tile(curr.x, curr.y - 1, tile)
                if west not in seen and west != prev:
                    if "E" in TILE_CONN[tile]:
                        seen.add(west)
                        return west
        case "E":
            # check east
            if curr.y + 1 < p.width:
                tile = p.tiles[curr.x][curr.y + 1]
                east = Tile(curr.x, curr.y + 1, tile)
                if east not in seen and east != prev:
                    if "W" in TILE_CONN[tile]:
                        seen.add(east)
                        return east
    return None


def next_tile(
    curr: Tile, p: Puzzle, seen: Set[Tile], prev: Optional[Tile] = None
) -> Optional[Tile]:
    """Find the next tile has not been [seen] yet and is not the [prev] tile
    (the one before the [curr] tile).

    The check for previous is needed to avoid a tile in the immediate
    vicinity of the [start] location returning [start] as the next tile at
    the beginning of the search. This can happen because the [start] location
    is never added to the [seen] set.
    """
    for dir in TILE_CONN[curr.tile]:
        if loc := peek_tile(dir, curr, p, seen, prev):
            return loc
    return None


def find_loop(p: Puzzle) -> List[Tile]:
    res: List[Tile] = [p.start]
    seen: Set[Tile] = set()
    while lres := len(res):
        prev: Optional[Tile] = res[-2] if lres > 1 else None
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


def find_poly_area(poly: List[Tile], puzzle: Puzzle) -> int:
    """
    Find the area of the polygon (i.e. number of locations within [poly] than
    are not on the polygon it's self.)
    """

    # Remove the poly locations from the puzzle tiles.
    # This is huge performance boost because it reduces the number of locations
    # to check to a very small fraction of the input.
    tiles = set(iter(puzzle)) - set(poly)

    def _is_in(loc: Tile) -> bool:
        """
        Count the number of [path] locations exist on a horizontal line before
        the given [loc] is reached.

        The tests pass *BUT* I don't really understand why disregarding [-JL]
        when scanning the tiles gives the correct result.

        See: https://en.wikipedia.org/wiki/Point_in_polygon
        """
        res = 0
        for p in poly:
            if p.x != loc.x:
                continue
            if p.y >= loc.y:
                continue
            if p.tile == "-" or p.tile == "J" or p.tile == "L":
                continue
            res += 1
        return res % 2 == 1

    _in = list(filter(_is_in, iter(tiles)))
    return len(_in)


def run(f: str):
    with open(f) as input:
        puzzle = parser.parse(input.read())
        print("Day 10: part 2 is {}".format(solve(puzzle)))


def solve(puzzle: Puzzle) -> int:
    return find_poly_area(find_loop(puzzle), puzzle)


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
                start = Tile(len(tiles), line.index("S"), "S")
            except ValueError:
                pass
        tiles.append(line)
        yield padding | eof
    if not start:
        raise Day10Error("Couldn't find the start location")
    return Puzzle(tiles, start, len(tiles[0]), len(tiles))
