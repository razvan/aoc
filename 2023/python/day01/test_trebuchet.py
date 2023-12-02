import unittest

import textwrap
from day01.trebuchet import trebuchet


class Day01TestCase(unittest.TestCase):
    def test_trebuchet(self):
        input: str = textwrap.dedent(
            """
            1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet
            """
        )
        self.assertEqual(142, trebuchet(input))
