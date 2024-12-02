from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        safe = 0
        for report in data:
            levels = [*map(int, report.split())]
            if self.is_safe(levels):
                safe += 1
        return safe

    def part2(self, data):
        safe = 0
        for report in data:
            levels = [*map(int, report.split())]
            if self.is_safe(levels):
                safe += 1
            else:
                for i in range(len(levels)):
                    tolerated_levels = levels[:i] + levels[i + 1 :]
                    if self.is_safe(tolerated_levels):
                        safe += 1
                        break
        return safe

    def is_safe(self, levels):
        differs = [a - b for a, b in zip(levels, levels[1:])]
        is_monotonic = all(i > 0 for i in differs) or all(i < 0 for i in differs)
        is_in_range = all(0 < abs(i) <= 3 for i in differs)
        if is_monotonic and is_in_range:
            return True
        return False
