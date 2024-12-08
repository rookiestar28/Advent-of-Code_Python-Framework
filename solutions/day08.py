from utils.solution_base import SolutionBase
from collections import defaultdict


class Solution(SolutionBase):
    def part1(self, data):
        _map = [list(line) for line in data]
        rows, cols = len(_map), len(_map[0])

        antennas = defaultdict(list)

        for row in range(rows):
            for col in range(cols):
                if _map[row][col] != ".":
                    antennas[_map[row][col]].append((row, col))

        antinodes = set()

        for antenna, coords in antennas.items():
            for i in range(len(coords)):
                for j in range(i + 1, len(coords)):
                    diff = tuple(a - b for a, b in zip(coords[j], coords[i]))

                    for _idx, _dir in [(i, -1), (j, 1)]:
                        pos = tuple([a + b * _dir for a, b in zip(coords[_idx], diff)])
                        if 0 <= pos[0] < rows and 0 <= pos[1] < cols:
                            antinodes.add(pos)

        return len(antinodes)

    def part2(self, data):
        _map = [list(line) for line in data]
        rows, cols = len(_map), len(_map[0])

        antennas = defaultdict(list)

        for row in range(rows):
            for col in range(cols):
                if _map[row][col] != ".":
                    antennas[_map[row][col]].append((row, col))

        antinodes = set()

        for antenna, coords in antennas.items():
            for i in range(len(coords)):
                for j in range(i + 1, len(coords)):
                    diff = tuple(a - b for a, b in zip(coords[j], coords[i]))

                    for _idx, _dir in [(i, -1), (j, 1)]:
                        pos = coords[_idx]
                        while 0 <= pos[0] < rows and 0 <= pos[1] < cols:
                            antinodes.add(pos)
                            pos = tuple([a + b * _dir for a, b in zip(pos, diff)])

        return len(antinodes)
