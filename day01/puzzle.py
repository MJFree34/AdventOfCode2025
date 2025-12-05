DIRECTIONS = {
    "L": -1,
    "R": 1,
}

initial_position = 50

def parse_input(input: str) -> [int]:
    for line in input.split("\n"):
        if line:
            direction = line[0]
            distance = int(line[1:])
            yield DIRECTIONS[direction] * distance

def solve_part1(rotations: [int]) -> int:
    position = initial_position
    num_zeroes = 0

    for rotation in rotations:
        position += rotation
        position %= 100
        if position == 0:
            num_zeroes += 1

    return num_zeroes

if __name__ == "__main__":
    with open("day01/input.txt", "r") as file:
        rotations = parse_input(file.read())

    print("Part 1: ", solve_part1(rotations))