from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def get_score(self, _map, i, j):
        rows, cols = len(_map), len(_map[0])
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        targets = []
        queue = [(i, j)]

        while queue:
            y, x = queue.pop(0)
            s = _map[y][x]
            _next = s + 1
            for dy, dx in dirs:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and _map[ny][nx] == _next:
                    if _next == 9:
                        targets.append((ny, nx))
                    else:
                        queue.append((ny, nx))

        return targets

    def part1(self, data):
        _map = [list(map(int, line)) for line in data]
        rows, cols = len(_map), len(_map[0])

        score = 0

        for i in range(rows):
            for j in range(cols):
                if _map[i][j] == 0:
                    targets = self.get_score(_map, i, j)
                    score += len(set(targets))
        return score

    def part2(self, data):
        _map = [list(map(int, line)) for line in data]
        rows, cols = len(_map), len(_map[0])

        score = 0

        for i in range(rows):
            for j in range(cols):
                if _map[i][j] == 0:
                    targets = self.get_score(_map, i, j)
                    score += len(targets)
        return score
