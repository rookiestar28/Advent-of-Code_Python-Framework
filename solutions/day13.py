from utils.solution_base import SolutionBase
import z3


class Solution(SolutionBase):
    def part1(self, data):
        machines = ("\n".join(data)).split("\n\n")
        coins = 0

        for machine in machines:
            btn_a, btn_b, prize = machine.split("\n")

            btn_a = [*map(lambda i: int(i[2:]), btn_a.split(": ")[1].split(", "))]
            btn_b = [*map(lambda i: int(i[2:]), btn_b.split(": ")[1].split(", "))]
            prize = [*map(lambda i: int(i[2:]), prize.split(": ")[1].split(", "))]

            s = z3.Solver()
            times_a, times_b = z3.Ints("times_a times_b")
            s.add(btn_a[0] * times_a + btn_b[0] * times_b == prize[0])
            s.add(btn_a[1] * times_a + btn_b[1] * times_b == prize[1])
            if s.check() == z3.sat:
                coins += s.model()[times_a].as_long() * 3 + s.model()[times_b].as_long()

        return coins

    def part2(self, data):
        machines = ("\n".join(data)).split("\n\n")
        coins = 0

        for machine in machines:
            btn_a, btn_b, prize = machine.split("\n")

            btn_a = [*map(lambda i: int(i[2:]), btn_a.split(": ")[1].split(", "))]
            btn_b = [*map(lambda i: int(i[2:]), btn_b.split(": ")[1].split(", "))]
            prize = [*map(lambda i: int(i[2:]) + 10000000000000, prize.split(": ")[1].split(", "))]

            s = z3.Solver()
            times_a, times_b = z3.Ints("times_a times_b")
            s.add(btn_a[0] * times_a + btn_b[0] * times_b == prize[0])
            s.add(btn_a[1] * times_a + btn_b[1] * times_b == prize[1])
            if s.check() == z3.sat:
                coins += s.model()[times_a].as_long() * 3 + s.model()[times_b].as_long()

        return coins
