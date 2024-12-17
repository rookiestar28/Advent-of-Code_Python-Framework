from utils.solution_base import SolutionBase


class Solution(SolutionBase):
    def run_program(self, registers, program):
        def combo_operand(value):
            match value:
                case 0 | 1 | 2 | 3:
                    return value
                case 4:
                    return A
                case 5:
                    return B
                case 6:
                    return C

        A, B, C = registers
        pointer = 0
        outputs = []

        while pointer < len(program):
            opcode = program[pointer]
            operand = program[pointer + 1]

            if opcode == 0:  # adv
                A //= 2 ** combo_operand(operand)
            elif opcode == 1:  # bxl
                B ^= operand
            elif opcode == 2:  # bst
                B = combo_operand(operand) % 8
            elif opcode == 3:  # jnz
                if A != 0:
                    pointer = operand
                    continue  # skip the pointer increment
            elif opcode == 4:  # bxc
                B ^= C
            elif opcode == 5:  # out
                outputs.append(combo_operand(operand) % 8)
            elif opcode == 6:  # bdv
                B = A // (2 ** combo_operand(operand))
            elif opcode == 7:  # cdv
                C = A // (2 ** combo_operand(operand))

            pointer += 2

        return outputs

    def part1(self, data):
        registers = [
            int(data[0].split(": ")[1]),
            int(data[1].split(": ")[1]),
            int(data[2].split(": ")[1]),
        ]
        program = list(map(int, data[4].split(": ")[1].split(",")))

        result = self.run_program(registers, program)
        return ",".join(map(str, result))

    def part2(self, data):
        program = list(map(int, data[4].split(": ")[1].split(",")))

        """
        after observing the output of run_program, I was found that a certain
        number of As form a fixed sequence of tail values
        so we could calculate the minimum value of the target answer and start looping
        """
        A = sum(7 * 8**i for i in range(len(program) - 1)) + 1

        while True:
            result = self.run_program([A, 0, 0], program)

            if len(result) > len(program):
                raise ValueError("The output is too long")

            if result == program:
                return A

            """
            after the tail numbers match, using the same approach to calculate how much
            needs to be added to adjust the next sequence interval to align with the
            previous number
            """
            add = 0
            for i in range(len(result) - 1, -1, -1):
                if result[i] != program[i]:
                    add = 8**i
                    A += add
                    break
