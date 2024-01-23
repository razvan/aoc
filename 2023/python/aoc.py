import day02
import day03
import day04
import day05
import day06
import day07
import day08
import day09
import day10
import day11
import day12
import sys


def main():
    match sys.argv[1]:
        case "day02":
            day02.main("../input/day02/input")
        case "day03":
            day03.main("../input/day02/input")
        case "day04":
            day04.main("../input/day04/input.txt")
        case "day05":
            day05.main("../input/day05/input.txt")
        case "day06":
            day06.main(["../input/day06/part1", "../input/day06/part2"])
        case "day07":
            day07.main(["../input/day07/input.txt"])
        case "day08":
            day08.main(["../input/day08/input.txt"])
        case "day09":
            day09.main(["../input/day09/input.txt"])
        case "day10":
            day10.main(["../input/day10/input.txt"])
        case "day11":
            day11.main(["../input/day11/input.txt"])
        case "day12":
            day12.main(["../input/day12/input.txt"])
        case _:
            day02.main("../input/day02/input")
            day03.main("../input/day03/input")
            day04.main("../input/day04/input.txt")
            day05.main("../input/day05/input.txt")
            day06.main(["../input/day06/part1", "../input/day06/part2"])
            day07.main(["../input/day07/input.txt"])
            day08.main(["../input/day08/input.txt"])
            day09.main(["../input/day09/input.txt"])
            day10.main(["../input/day10/input.txt"])
            day11.main(["../input/day11/input.txt"])
            day12.main(["../input/day12/input.txt"])


if __name__ == "__main__":
    main()
