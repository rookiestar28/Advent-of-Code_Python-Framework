from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def parse_data(self, data):
        grid = []
        coords_by_type = {}
        rows, cols = len(data), len(data[0])
        for row in range(rows):
            line = list(data[row].strip())
            grid.append(line)
            for col in range(cols):
                _type = line[col]
                if _type not in coords_by_type:
                    coords_by_type[_type] = set()
                coords_by_type[_type].add((row, col))
        return grid, coords_by_type

    def get_curr_group(self, grid, coord):
        y, x = coord
        _type = grid[y][x]
        rows, cols = len(grid), len(grid[0])

        adjs = set()
        stack = [(y, x)]
        while stack:
            y, x = stack.pop()
            if (y, x) in adjs:
                continue
            adjs.add((y, x))
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols and grid[ny][nx] == _type:
                    stack.append((ny, nx))
        return adjs

    def part1(self, data):
        grid, coords_by_type = self.parse_data(data)
        types = set(coords_by_type.keys())

        def get_connected_count(grid, coord):
            rows, cols = len(grid), len(grid[0])
            y, x = coord
            count = 0
            for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                ny, nx = y + dy, x + dx
                if 0 <= ny < rows and 0 <= nx < cols:
                    count += grid[ny][nx] == grid[y][x]
            return count

        prices = {}
        for _type in types:
            prices[_type] = 0
            coords = coords_by_type[_type]

            while coords:
                curr = coords.pop()
                curr_group = self.get_curr_group(grid, curr)
                coords -= curr_group
                connected_count = {}  # count of connected sides for each cell in the group
                for coord in curr_group:
                    connected_count[coord] = get_connected_count(grid, coord)

                price = len(curr_group) * (len(curr_group) * 4 - sum(connected_count.values()))
                prices[_type] += price

        return sum(prices.values())

    def part2(self, data):
        grid, coords_by_type = self.parse_data(data)
        types = set(coords_by_type.keys())

        def get_group_sides(group):
            min_y = min(group, key=lambda x: x[0])[0]
            max_y = max(group, key=lambda x: x[0])[0]
            min_x = min(group, key=lambda x: x[1])[1]
            max_x = max(group, key=lambda x: x[1])[1]
            rows = max_y - min_y + 1
            cols = max_x - min_x + 1
            new_group = [(y - min_y, x - min_x) for y, x in group]

            # create grid, add 1 more space around the group
            grid = [[" " for _ in range(cols + 2)] for _ in range(rows + 2)]
            for y, x in new_group:
                grid[y + 1][x + 1] = "X"

            sides = 0

            for _ in range(2):
                for y in range(1, rows + 1):
                    # count from top to bottom
                    sides += len("".join(["X" if current != above and current == "X" else " " for current, above in zip(grid[y], grid[y - 1])]).split())

                    # upside down
                    sides += len("".join(["X" if current != above and current == "X" else " " for current, above in zip(grid[y], grid[y + 1])]).split())

                # rotate grid 90 degrees
                grid = list(zip(*grid[::-1]))
                rows, cols = cols, rows

            return sides

        prices = {}
        for _type in types:
            prices[_type] = 0
            coords = coords_by_type[_type]

            while coords:
                coord = coords.pop()
                curr_group = self.get_curr_group(grid, coord)
                coords -= curr_group

                group_sides = get_group_sides(curr_group)

                price = len(curr_group) * group_sides
                prices[_type] += price

        return sum(prices.values())
