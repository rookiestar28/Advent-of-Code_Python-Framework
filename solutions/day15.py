from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    dirs = {
        "^": (-1, 0),
        "v": (1, 0),
        "<": (0, -1),
        ">": (0, 1),
    }

    def get_robot_pos(self, grid):
        rows, cols = len(grid), len(grid[0])
        for i in range(rows):
            for j in range(cols):
                if grid[i][j] == "@":
                    return (i, j)

    def moving(self, grid, pos, moves, part):
        for move in moves:
            """
            # zip looks nice but way too slow
            ny, nx = (a + b for a, b in zip(pos, self.dirs[move]))
            """
            ny = pos[0] + self.dirs[move][0]
            nx = pos[1] + self.dirs[move][1]

            if grid[ny][nx] == ".":
                pos = (ny, nx)
            elif grid[ny][nx] == "#":
                continue
            else:
                edges, adjs = self.get_adjs_and_edges(grid, pos, move, part)
                blocked = 0
                dy, dx = self.dirs[move]
                for cell in edges:
                    ny, nx = (cell[0] + dy, cell[1] + dx)
                    if grid[ny][nx] == "#":
                        blocked += 1
                if blocked == 0:
                    grid = self.update_grid(grid, adjs, move)
                    pos = (pos[0] + dy, pos[1] + dx)
        return grid

    def get_adjs_and_edges(self, grid, pos, move, part=1):
        y, x = pos
        dy, dx = self.dirs[move]

        adjs = set()
        if part == 1 or move in "<>":
            while True:
                ny, nx = y + dy, x + dx
                if grid[ny][nx] in ".#":
                    return [(ny - dy, nx - dx)], adjs
                y = ny
                x = nx
                adjs.add((y, x))
        else:
            edges = []
            queue = [(y, x)]
            while queue:
                y, x = queue.pop(0)
                if (y, x) in adjs:
                    continue
                adjs.add((y, x))
                ny, nx = y + dy, x + dx
                if grid[ny][nx] in ".#":
                    edges.append((y, x))
                elif grid[ny][nx] == "[":
                    queue.append((ny, nx))
                    queue.append((ny, nx + 1))
                elif grid[ny][nx] == "]":
                    queue.append((ny, nx))
                    queue.append((ny, nx - 1))

            return edges, adjs - {(pos[0], pos[1])}

    def update_grid(self, grid, visited, move):
        cells = []
        match move:
            case "^":
                cells = sorted(visited, key=lambda x: x[0])
            case "v":
                cells = sorted(visited, key=lambda x: x[0], reverse=True)
            case "<":
                cells = sorted(visited, key=lambda x: x[1])
            case ">":
                cells = sorted(visited, key=lambda x: x[1], reverse=True)
        dy, dx = self.dirs[move]
        for cell in cells:
            y, x = cell
            ny, nx = y + dy, x + dx
            grid[ny][nx] = grid[y][x]
            grid[y][x] = "."
        return grid

    def get_coords_sum(self, grid, part=1):
        target = "[" if part == 2 else "O"
        rows, cols = len(grid), len(grid[0])
        # _sum = 0
        # for r in range(rows):
        #     for c in range(cols):
        #         if grid[r][c] == target:
        #             _sum += 100 * r + c
        _sum = sum(100 * r + c for r in range(rows) for c in range(cols) if grid[r][c] == target)
        return _sum

    def resize_grid(self, grid):
        _mappings = {
            "#": "##",
            "O": "[]",
            ".": "..",
            "@": "@.",
        }
        # new_grid = []
        # for line in grid:
        #     new_line = list("".join(_mappings[c] for c in line))
        #     new_grid.append(new_line)
        new_grid = [list("".join(_mappings[c] for c in line)) for line in grid]
        return new_grid

    def part1(self, data):
        part = 1
        grid, moves = "\n".join(data).split("\n\n")
        grid = [list(row) for row in grid.split("\n")]
        moves = list("".join(moves.split("\n")))

        pos = self.get_robot_pos(grid)
        grid[pos[0]][pos[1]] = "."

        grid = self.moving(grid, pos, moves, part)
        _sum = self.get_coords_sum(grid, part)
        return _sum

    def part2(self, data):
        part = 2
        grid, moves = "\n".join(data).split("\n\n")
        grid = [list(row) for row in grid.split("\n")]
        moves = list("".join(moves.split("\n")))

        grid = self.resize_grid(grid)

        pos = self.get_robot_pos(grid)
        grid[pos[0]][pos[1]] = "."

        grid = self.moving(grid, pos, moves, part)
        _sum = self.get_coords_sum(grid, part)
        return _sum
