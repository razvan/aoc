"""
https://adventofcode.com/2023/day/2
"""

import re
from enum import Enum
from typing import List, Optional, Dict, Tuple

COLOR = {"red": 0, "green": 1, "blue": 2}
State = Enum("State", ["START", "GAME", "CUBE"])


def possible_games(games: str, total_cubes: Tuple[int, int, int]) -> List[int]:
    """Return the game ids that would have been possible given total_cubes."""
    result: List[int] = []
    max_cubes_per_game = parse_games(games)
    for gid, cubes in max_cubes_per_game.items():
        if (
            cubes[COLOR["red"]] <= total_cubes[COLOR["red"]]
            and cubes[COLOR["green"]] <= total_cubes[COLOR["green"]]
            and cubes[COLOR["blue"]] <= total_cubes[COLOR["blue"]]
        ):
            result.append(gid)
    return result


def parse_games(games: str) -> Dict[int, List[int]]:
    """For each game, extract the max cubes per color.
    Return:
        dict: key is the game id, value is the max cubes per color
    """
    cubes: Dict[int, List[int]] = {}
    for game in games.splitlines():
        state: State = State.START
        gid: Optional[int] = None
        value = None
        game_cubes: List[int] = [0, 0, 0]
        for token in re.split("[ :;,]+", game):
            if state == State.START and token == "Game":
                state = State.GAME
                continue
            elif state == State.GAME:
                gid = int(token)
                state = State.CUBE
                continue
            elif state == State.CUBE:
                if token.isnumeric():
                    value = int(token)
                    continue
                elif token in COLOR:
                    game_cubes[COLOR[token]] = max(game_cubes[COLOR[token]], value)
        if gid:
            cubes[gid] = game_cubes
    return cubes
