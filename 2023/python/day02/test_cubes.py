import unittest

import textwrap
from day02.cubes import parse_games, possible_games, cube_set_power


class Day02TestCase(unittest.TestCase):
    input: str = textwrap.dedent(
        """
        Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
        Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
        Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
        Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
        Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
        """
    )

    def test_parse_games(self):
        result = parse_games(self.input)
        self.assertEqual(5, len(result))

    def test_possible_games(self):
        pgames = possible_games(self.input, (12, 13, 14))
        self.assertEqual(pgames, [1, 2, 5])

    def test_sum_id_possible_games(self):
        pgames = possible_games(self.input, (12, 13, 14))
        self.assertEqual(sum(pgames), 8)

    def test_cube_set_power(self):
        # 4,2,6      48
        # 1,3,4      12
        # 20,13,6    1560
        # 14,3,15    630
        # 6,3,2      36
        self.assertEqual(cube_set_power(self.input), 2286)
