from utils.solution_base import SolutionBase
from collections import defaultdict


class Solution(SolutionBase):
    def extract_data(self, data):
        _sep = data.index("")

        rules = defaultdict(set)
        for i in data[:_sep]:
            a, b = map(int, i.split("|"))
            rules[a].add(b)

        updates = [list(map(int, i.split(","))) for i in data[_sep + 1 :]]

        return rules, updates

    def is_valid(self, rules, update):
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if update[j] not in rules[update[i]]:
                    return False
        return True

    def fix_update(self, rules, update):
        filtered_rules = defaultdict(set)
        for i in update:
            filtered_rules[i] = rules[i] & set(update)

        # ordered_items = sorted(filtered_rules.items(), key=lambda x: len(x[1]), reverse=True)
        # ordered_keys = [i[0] for i in ordered_items]
        ordered_keys = sorted(filtered_rules, key=lambda k: len(filtered_rules[k]), reverse=True)

        return ordered_keys

    def part1(self, data):
        rules, updates = self.extract_data(data)
        add_up = 0

        for update in updates:
            if self.is_valid(rules, update):
                add_up += update[len(update) // 2]

        return add_up

    def part2(self, data):
        rules, updates = self.extract_data(data)
        add_up = 0

        for update in updates:
            if not self.is_valid(rules, update):
                fixed_update = self.fix_update(rules, update)
                add_up += fixed_update[len(update) // 2]

        return add_up
