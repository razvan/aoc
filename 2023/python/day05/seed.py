import sys
from .model import Almanac
from .parser import almanac


def main(f: str):
    with open(f) as input:
        strin = input.read()
        a: Almanac = almanac.parse(strin)
        print("Day 05: min location is {}".format(a.min_location()))


if __name__ == "__main__":
    main(sys.argv[1])
