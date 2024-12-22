from utils.solution_base import SolutionBase
from collections import defaultdict
from functools import cache


class Solution(SolutionBase):
    def parse_moves(self, keypad):
        def get_key_pos(keypad):
            pos = {}
            for r, row in enumerate(keypad):
                for c, key in enumerate(row):
                    pos[key] = (r, c)
            return pos

        pos = get_key_pos(keypad)
        keys = sorted(pos.keys())

        moves = defaultdict(list)
        for key1 in keys:
            for key2 in keys:
                if key1 == "#" or key2 == "#" or key1 == key2:
                    continue
                p1 = pos[key1]
                p2 = pos[key2]

                if p1[0] == p2[0]:
                    d = ">" if p2[1] > p1[1] else "<"
                    moves[(key1, key2)].append(d * (abs(p2[1] - p1[1])) + "A")
                elif p1[1] == p2[1]:
                    d = "v" if p2[0] > p1[0] else "^"
                    moves[(key1, key2)].append(d * (abs(p2[0] - p1[0])) + "A")
                else:
                    if p1[0] != pos["#"][0] or p2[1] != pos["#"][1]:
                        d1 = ">" if p2[1] > p1[1] else "<"
                        d2 = "v" if p2[0] > p1[0] else "^"
                        moves[(key1, key2)].append(d1 * (abs(p2[1] - p1[1])) + d2 * (abs(p2[0] - p1[0])) + "A")
                    if p1[1] != pos["#"][1] or p2[0] != pos["#"][0]:
                        d1 = "v" if p2[0] > p1[0] else "^"
                        d2 = ">" if p2[1] > p1[1] else "<"
                        moves[(key1, key2)].append(d1 * (abs(p2[0] - p1[0])) + d2 * (abs(p2[1] - p1[1])) + "A")
        return moves

    def build_combinations(self, arrays, current=[], index=0):
        if index == len(arrays):
            return [current]
        results = []
        for value in arrays[index]:
            new_results = self.build_combinations(arrays, current + [value], index + 1)
            results.extend(new_results)
        return results

    @cache
    def translate(self, code, depth):
        if code[0].isnumeric():
            moves = self.translate_numpad(code)
        else:
            moves = self.translate_keypad(code)

        if depth == 0:
            return min([sum(map(len, move)) for move in moves])
        else:
            return min([sum(self.translate(curr_code, depth - 1) for curr_code in move) for move in moves])

    def translate_numpad(self, code):
        code = "A" + code
        moves = [self.moves1[(a, b)] for a, b in zip(code, code[1:])]
        moves = self.build_combinations(moves)
        return moves

    def translate_keypad(self, code):
        code = "A" + code
        moves = [self.moves2[(a, b)] if a != b else ["A"] for a, b in zip(code, code[1:])]
        moves = self.build_combinations(moves)
        return moves

    def part1(self, data):
        keypad1 = ["789", "456", "123", "#0A"]
        keypad2 = ["#^A", "<v>"]

        self.moves1 = self.parse_moves(keypad1)
        self.moves2 = self.parse_moves(keypad2)

        complexities = 0

        for code in data:
            min_len = self.translate(code, 2)
            # print(min_len, int(code[:-1]))
            complexities += min_len * int(code[:-1])

        return complexities

    def part2(self, data):
        keypad1 = ["789", "456", "123", "#0A"]
        keypad2 = ["#^A", "<v>"]

        self.moves1 = self.parse_moves(keypad1)
        self.moves2 = self.parse_moves(keypad2)

        complexities = 0

        for code in data:
            min_len = self.translate(code, 25)
            # print(min_len, int(code[:-1]))
            complexities += min_len * int(code[:-1])

        return complexities
