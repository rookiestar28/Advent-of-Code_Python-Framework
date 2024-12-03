from utils.solution_base import SolutionBase
import re


class Solution(SolutionBase):
    def part1(self, data):
        pattern = r"mul\((\d{1,3}),(\d{1,3})\)"
        matches = re.findall(pattern, "".join(data))

        result = sum(int(x) * int(y) for x, y in matches)

        return result

    def part2(self, data):
        pattern = r"(mul\((\d{1,3}),(\d{1,3})\)|do\(\)|don't\(\))"
        instructions = re.findall(pattern, "".join(data))

        enabled = True
        result = 0

        for inst in instructions:
            match inst[0]:
                case "do()":
                    enabled = True
                case "don't()":
                    enabled = False
                case _ if enabled:
                    result += int(inst[1]) * int(inst[2])

        return result
