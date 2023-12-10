from parsy import regex, string, seq, eof, whitespace
from typing import List

from .model import Dice, GameDraw, Game


p_optional_space = regex(r"\s*")
p_space = regex(r"\s+")
p_game = string("Game")
p_num = regex(r"\d+")
p_colon = string(":")
p_comma = string(",")
p_semi = string(";")
p_red = string("red")
p_green = string("green")
p_blue = string("blue")
p_eol = string("\n")

p_color = (p_red | p_green | p_blue).desc("color can only be red, green or blue")
p_side = seq(_s1=p_space, num=p_num.map(int), _s2=p_space, color=p_color).combine_dict(
    Dice
)
p_draw = p_side.sep_by(p_comma, min=1).combine(lambda *d: GameDraw(dices=d))
p_line = seq(
    _g=p_optional_space >> p_game >> p_space,
    id=p_num.map(int),
    _c=p_colon,
    draws=p_draw.sep_by(p_semi),
    _e=(eof | p_eol | (whitespace >> p_eol)),
).combine_dict(Game)

p_games = p_line.many()


def parse(input: str) -> List[Game]:
    return p_games.parse(input)
