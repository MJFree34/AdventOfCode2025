from enum import Enum

class ProblemType(Enum):
    MULT = "*"
    ADD = "+"

class Problem:
    def __init__(self, numbers, problem_type):
        self.numbers = numbers
        self.problem_type = ProblemType(problem_type)

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

def parse_input(input):
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

def solve_part1(input):
    results_sum = 0
    for problem in input:
        results_sum += problem.solve()
    return results_sum

if __name__ == "__main__":
    with open("day06/input.txt", "r") as file:
        input = parse_input(file.read())

    print("Part 1:", solve_part1(input))