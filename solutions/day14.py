from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def part1(self, data):
        robots = []
        for line in data:
            a, b = line.split(" ")
            x, y = map(int, a[2:].split(","))
            vx, vy = map(int, b[2:].split(","))
            robots.append(((x, y), (vx, vy)))

        width = 101
        height = 103

        # for the test input
        if len(robots) == 12:
            width = 11
            height = 7

        quads = [0, 0, 0, 0]

        for i in range(len(robots)):
            (x, y), (vx, vy) = robots[i]
            x = (x + 100 * (vx + width)) % width
            y = (y + 100 * (vy + height)) % height

            if x == width // 2 or y == height // 2:
                continue

            quad_idx = (int(x > width // 2)) + (int(y > height // 2) * 2)
            quads[quad_idx] += 1

        return quads[0] * quads[1] * quads[2] * quads[3]

    def part2(self, data):

        robots = []
        for line in data:
            a, b = line.split(" ")
            x, y = map(int, a[2:].split(","))
            vx, vy = map(int, b[2:].split(","))
            robots.append(((x, y), (vx, vy)))

        width = 101
        height = 103

        t = 0

        while True:
            t += 1
            pos = set()
            valid = True

            for (x, y), (vx, vy) in robots:
                x = (x + t * (vx + width)) % width
                y = (y + t * (vy + height)) % height
                if (x, y) in pos:
                    valid = False
                    break
                pos.add((x, y))

            if valid:
                return t
