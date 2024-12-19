from utils.solution_base import SolutionBase
from collections import defaultdict


class Solution(SolutionBase):
    def part1(self, data):
        towels = sorted(data[0].split(", "), key=len)
        designs = data[2:]

        count = 0
        for design in designs:
            if self.is_valid_design(design, towels):
                count += 1
        return count

    def is_valid_design(self, design, towels):
        def matching_towel(pos):
            if pos == len(design):
                return True

            for towel in towels:
                next_pos = pos + len(towel)
                if next_pos <= len(design) and design[pos:next_pos] == towel:
                    if matching_towel(next_pos):
                        return True

            return False

        return matching_towel(0)

    def part2(self, data):
        towels = sorted(data[0].split(", "), key=len)
        designs = data[2:]

        total = 0
        for design in designs:
            total += self.get_valid_count(design, towels)
        return total

    def get_valid_count(self, design, towels):
        cache = defaultdict(int)

        def matching_towel(pos):
            if pos == len(design):
                return 1

            if cache[pos] > 0:
                return cache[pos]

            matches = 0
            for towel in towels:
                next_pos = pos + len(towel)
                if next_pos <= len(design) and design[pos:next_pos] == towel:
                    matches += matching_towel(next_pos)

            cache[pos] = matches
            return matches

        return matching_towel(0)
