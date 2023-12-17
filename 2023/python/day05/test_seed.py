from unittest import TestCase
import textwrap
from .model import Range, RangeMap
from .parser import almanac, seeds, env_map


class Day05TestCase(TestCase):
    input = textwrap.dedent(
        """
        seeds: 79 14 55 13

        seed-to-soil map:
        50 98 2
        52 50 48

        soil-to-fertilizer map:
        0 15 37
        37 52 2
        39 0 15

        fertilizer-to-water map:
        49 53 8
        0 11 42
        42 0 7
        57 7 4

        water-to-light map:
        88 18 7
        18 25 70

        light-to-temperature map:
        45 77 23
        81 45 19
        68 64 13

        temperature-to-humidity map:
        0 69 1
        1 0 69

        humidity-to-location map:
        60 56 37
        56 93 4
        """
    )

    def test_range_single(self):
        _range = Range(0, 47, 3)
        got = [_range.dest(x) for x in range(46, 51)]
        self.assertEqual([None, 0, 1, 2, None], got)

    def test_range_map_single(self):
        rm = RangeMap("", [Range(50, 98, 2), Range(52, 50, 48)])
        got = [rm.dest(49), rm.dest(61), rm.dest(98), rm.dest(3)]
        expected = [49, 63, 50, 3]
        self.assertEqual(expected, got)

    def test_parse_seeds(self):
        self.assertEqual([79, 14, 55, 13], seeds.parse("seeds: 79 14 55 13"))

    def test_parse_env_map(self):
        got = env_map.parse(
            """temperature-to-humidity map:
                0 69 1
                1 0 69
            """
        )
        expected = RangeMap(
            name="temperature-to-humidity map:",
            ranges=[Range(0, 69, 1), Range(1, 0, 69)],
        )
        self.assertEqual(expected, got)

    def test_parse_almanac(self):
        a = almanac.parse(self.input)
        self.assertEqual(7, len(a.rangemaps))
        self.assertEqual("humidity-to-location map:", a.rangemaps[-1].name)
        self.assertEqual(2, len(a.rangemaps[-1].ranges))

    def test_min_location(self):
        a = almanac.parse(self.input)
        self.assertTrue(35, a.min_location())

    def test_min_location_seed_ranges(self):
        a = almanac.parse(self.input)
        self.assertTrue(46, a.min_location_seed_ranges())

    def test_min_loc_seed_range2(self):
        """
        79, 80, ..., 89, 90, 91, 92, 93
        55, 56, ..., 65, 66, 67, 68

        55 -> 57
        """
        input = textwrap.dedent(
            """
            seeds: 79 14 55 13

            seed-to-soil map:
            50 98 2
            52 50 48
            """
        )
        a = almanac.parse(input)
        self.assertTrue(57, a.min_location_seed_ranges())

    def test_min_loc_seed_range3(self):
        """
        79, 80, ..., 89, 90, 91, 92, 93
        55, 56, ..., 65, 66, 67, 68

        55 -> 57
        """
        input = textwrap.dedent(
            """
            seeds: 79 14 55 13

            seed-to-soil map:
            50 98 2
            52 50 48

            soil-to-fertilizer map:
            0 15 37
            37 52 2
            39 0 15
            """
        )
        a = almanac.parse(input)
        self.assertTrue(37, a.min_location_seed_ranges())
