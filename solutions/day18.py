from utils.solution_base import SolutionBase
import networkx as ntx


class Solution(SolutionBase):
    use_networkx = False
    grid = None
    graph = None
    size = None
    corrupted = None
    corrupted_length = None

    def parse_data(self, data):
        self.corrupted = [[*map(int, line.split(","))] for line in data]

        self.size = 71
        self.corrupted_length = 1024

        if len(self.corrupted) == 25:  # test input
            self.size = 7
            self.corrupted_length = 12

        self.set_grid()

    def set_grid(self):
        self.grid = [["."] * self.size for _ in range(self.size)]
        for x, y in self.corrupted[: self.corrupted_length]:
            self.grid[y][x] = "#"

        if self.use_networkx:
            self.graph = ntx.Graph()
            for y in range(self.size):
                for x in range(self.size):
                    if self.grid[y][x] == ".":
                        self.graph.add_node((x, y))
                        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < self.size and 0 <= ny < self.size and self.grid[ny][nx] == ".":
                                self.graph.add_edge((x, y), (nx, ny))

    def add_corrupted(self, cx, cy):
        if self.grid is not None:
            self.grid[cy][cx] = "#"

        if self.use_networkx and self.graph is not None:
            self.graph.remove_node((cx, cy))

    def get_shortest_path_steps(self):
        size = len(self.grid)

        start = (0, 0)
        end = (size - 1, size - 1)

        if self.use_networkx:
            try:
                path = ntx.shortest_path(self.graph, start, end)
                return len(path) - 1
            except ntx.exception.NetworkXNoPath:
                return -1
        else:
            # BFS
            queue = [(start, 0)]  # pos, length
            seen = set()
            while queue:
                pos, length = queue.pop(0)
                if pos == end:
                    return length
                if pos in seen:
                    continue
                seen.add(pos)
                x, y = pos
                for dx, dy in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size and self.grid[ny][nx] == ".":
                        queue.append(((nx, ny), length + 1))
            return -1  # no path

    def part1(self, data):
        # self.use_networkx = True
        self.parse_data(data)
        steps = self.get_shortest_path_steps()
        return steps

    def part2(self, data):
        self.use_networkx = True
        self.parse_data(data)
        for cx, cy in self.corrupted[self.corrupted_length :]:
            self.add_corrupted(cx, cy)
            steps = self.get_shortest_path_steps()
            if steps == -1:
                return f"{cx},{cy}"
