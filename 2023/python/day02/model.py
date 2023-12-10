from dataclasses import dataclass
from typing import List, Tuple
from enum import StrEnum, auto
from math import prod


class Color(StrEnum):
    Red = auto()
    Green = auto()
    Blue = auto()


@dataclass(slots=True, frozen=True, repr=True)
class Dice:
    num: int
    color: Color


@dataclass(slots=True, frozen=True, repr=True)
class GameDraw:
    dices: List[Dice]


@dataclass(slots=True, frozen=True, repr=True)
class Game:
    id: int
    draws: List[GameDraw]

    def max_dice(self) -> Tuple[int, int, int]:
        res: Tuple[int, int, int] = (0, 0, 0)
        for draw in self.draws:
            for dice in draw.dices:
                match dice:
                    case Dice(num=n, color=Color.Red):
                        res = (max(res[0], n), res[1], res[2])
                    case Dice(num=n, color=Color.Green):
                        res = (res[0], max(res[1], n), res[2])
                    case Dice(num=n, color=Color.Blue):
                        res = (res[0], res[1], max(res[2], n))
        return res

    def power(self) -> int:
        return prod(self.max_dice())
