import unittest

from day03.gear import parse_engine_schema


class Day03TestCase(unittest.TestCase):
    input: str = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
.........1
"""

    def test_parse_engine_schema_1(self):
        es = parse_engine_schema(self.input)
        self.assertEqual(es.dim(), (11, 10))

    def test_parse_engine_schema_2(self):
        es = parse_engine_schema(self.input)
        got = [es.schema[(0, 0)], es.schema[(3, 6)], es.schema[(9, 9)]]
        self.assertEqual(got, ["4", "#", "."])

    def test_symloc(self):
        es = parse_engine_schema(self.input)
        got = [es.symloc(3, 6), es.symloc(0, 3)]
        self.assertTrue(got, [True, False])

    def test_codes(self):
        es = parse_engine_schema(self.input)
        codes = es.codes()
        self.assertEqual(
            codes,
            [
                (0, 0, "467"),
                (0, 5, "114"),
                (2, 2, "35"),
                (2, 6, "633"),
                (4, 0, "617"),
                (5, 7, "58"),
                (6, 2, "592"),
                (7, 6, "755"),
                (9, 1, "664"),
                (9, 5, "598"),
                (10, 9, "1"),
            ],
        )

    def test_adjacent_sym(self):
        es = parse_engine_schema(self.input)
        self.assertTrue(es.adjacent_sym(0, 0, 3))  # 467, True
        self.assertTrue(es.adjacent_sym(2, 2, 2))  # 35,  True
        self.assertTrue(es.adjacent_sym(2, 6, 3))  # 633, True
        self.assertTrue(es.adjacent_sym(4, 0, 3))  # 617, True
        self.assertTrue(es.adjacent_sym(6, 2, 3))  # 592, True
        self.assertTrue(es.adjacent_sym(7, 6, 3))  # 755, True
        self.assertTrue(es.adjacent_sym(9, 1, 3))  # 664, True
        self.assertTrue(es.adjacent_sym(9, 5, 3))  # 598, True

        self.assertFalse(es.adjacent_sym(0, 5, 3))  # 114, False
        self.assertFalse(es.adjacent_sym(5, 7, 2))  # 58,  False
        self.assertFalse(es.adjacent_sym(10, 9, 1))  # 1,   False

    def test_gear_ratios(self):
        es = parse_engine_schema(self.input)
        self.assertEqual(es.gear_ratios(), [467, 35, 633, 617, 592, 755, 664, 598])
