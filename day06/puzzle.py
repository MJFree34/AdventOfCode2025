from enum import Enum

class ProblemType(Enum):
    MULT = "*"
    ADD = "+"

class Problem:
    def __init__(self, numbers, type_string):
        self.numbers = numbers
        self.problem_type = ProblemType(type_string)

    def solve(self):
        if self.problem_type == ProblemType.ADD:
            return sum(self.numbers)
        elif self.problem_type == ProblemType.MULT:
            result = 1
            for number in self.numbers:
                result *= number
            return result
        else:
            raise ValueError(f"Unknown problem type: {self.problem_type}")

    def __str__(self):
        return f"Problem(numbers={self.numbers}, problem_type={self.problem_type})"

def parse_input_part1(input):
    number_grid = []
    lines = input.split('\n')

    for i, line in enumerate(lines):
        if i != len(lines) - 1:
            number_grid.append([int(x) for x in line.split()])
        else:
            problems = []
            for j, type_string in enumerate(line.split()):
                numbers = [number_grid[k][j] for k in range(0, len(lines) - 1)]
                problem = Problem(numbers, type_string)
                # print(problem)
                problems.append(problem)

    return problems

def transform_column(column_numbers):
    # print(f"Transforming column: {column_numbers}")
    numbers = []
    for position in range(len(column_numbers[0])):
        # print(f"  Position: {position}")
        power = 1
        number = 0
        for column in reversed(column_numbers):
            # print(f"    Column: {column}, char: '{column[position]}'")
            if column[position] != ' ':
                number += int(column[position]) * power
                power *= 10
        numbers.append(number)
    # print(numbers)
    return numbers

def parse_input_part2(input):
    lines = input.split('\n')
    problems = []

    column_start_index = 0
    type_str = lines[-1][0]

    for i, c in enumerate(lines[-1]):
        if c in ('*', '+') and i != 0:
            column = []
            for line in lines[:-1]:
                column.append(line[column_start_index:i - 1])

            problem = Problem(transform_column(column), type_str)
            # print(problem)
            problems.append(problem)

            column_start_index = i
            type_str = c

    column = []
    for line in lines[:-1]:
        column.append(line[column_start_index:])
    problem = Problem(transform_column(column), type_str)
    # print(problem)
    problems.append(problem)

    return problems

def solve(input):
    results_sum = 0
    for problem in input:
        results_sum += problem.solve()
    return results_sum

if __name__ == "__main__":
    with open("day06/input.txt", "r") as file:
        input_str = file.read()
        part1_input = parse_input_part1(input_str)
        part2_input = parse_input_part2(input_str)

    print("Part 1:", solve(part1_input))

    print("Part 2:", solve(part2_input))