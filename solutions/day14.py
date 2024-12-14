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

        # there’s no need to loop 100 times
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
        """
        notes:

        I initially printed every single frame but then realized there was a
        10403-frame pattern. Within that pattern, I noticed a sus frame that
        appears every 101 frames, where a bunch of robots clustering into a
        vertical thick line. I focused on those frames and eventually found
        the answer.

        Then, I saw someone mention that no robot stands in the same spot when
        they form the Christmas tree. That completely blew my mind...
        """
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
