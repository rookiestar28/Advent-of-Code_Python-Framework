from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        _left, _right = zip(*[map(int, line.split()) for line in data])
        distance = sum(abs(x - y) for x, y in zip(sorted(_left), sorted(_right)))

        return distance

    def part2(self, data):
        _left, _right = zip(*[map(int, line.split()) for line in data])
        score = sum(x * _right.count(x) for x in _left)

        return score
