from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def parse_data(self, data):
        grid, start, end = [], None, None
        for r in range(len(data)):
            row = list(data[r])
            grid.append(row)
            for c in range(len(row)):
                if row[c] == "S":
                    start = (r, c)
                elif row[c] == "E":
                    end = (r, c)
        return grid, start, end

    def find_shortest_path(self, grid, start, end):
        rows, cols = len(grid), len(grid[0])
        visited = set()

        queue = [(start, 0, [start])]  # position, steps, path
        visited.add(start)

        while queue:
            (r, c), steps, path = queue.pop(0)
            if (r, c) == end:
                return steps, path

            for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if 0 < nr < rows - 1 and 0 < nc < cols - 1 and grid[nr][nc] != "#" and (nr, nc) not in visited:
                    new_path = path + [(nr, nc)]
                    queue.append(((nr, nc), steps + 1, new_path))
                    visited.add((nr, nc))

    def find_cheatable_pairs(self, path, savings, cheat_moves):
        pairs = set()

        for i in range(len(path) - savings):
            for j in range(i + 1 + savings, len(path)):
                p1 = path[i]
                p2 = path[j]
                manhattan = abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
                if (manhattan <= cheat_moves) and (savings <= j - i - manhattan):
                    pairs.add((path[i], path[j]))
        return len(pairs)

    def find_cheatable_pairs_in_range(self, path, savings, cheat_moves):
        cheats = 0

        coords_steps = {}
        for i, coord in enumerate(path):
            coords_steps[coord] = i

        possible_ranges = []
        for dy in range(-cheat_moves, cheat_moves + 1):
            for dx in range(-cheat_moves, cheat_moves + 1):
                if dy == 0 and dx == 0:
                    continue

                manhattan = abs(dy) + abs(dx)
                if manhattan > cheat_moves:
                    continue

                possible_ranges.append((dy, dx, manhattan))

        for y, x in path:
            for dy, dx, manhattan in possible_ranges:
                ny, nx = y + dy, x + dx
                if (ny, nx) in coords_steps:
                    if savings <= (coords_steps[(ny, nx)] - coords_steps[(y, x)] - manhattan):
                        cheats += 1
        return cheats

    def part1(self, data):
        grid, start, end = self.parse_data(data)
        steps, path = self.find_shortest_path(grid, start, end)

        savings = 100
        cheat_moves = 2

        # cheatable_count = self.find_cheatable_pairs(path, savings, cheat_moves)
        cheatable_count = self.find_cheatable_pairs_in_range(path, savings, cheat_moves)
        return cheatable_count

    def part2(self, data):
        grid, start, end = self.parse_data(data)
        steps, path = self.find_shortest_path(grid, start, end)

        savings = 100
        cheat_moves = 20

        # cheatable_count = self.find_cheatable_pairs(path, savings, cheat_moves)
        cheatable_count = self.find_cheatable_pairs_in_range(path, savings, cheat_moves)
        return cheatable_count
