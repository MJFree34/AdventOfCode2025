DIRECTIONS = {
    "L": -1,
    "R": 1,
}

initial_position = 50

def parse_input(input):
    return [DIRECTIONS[line[0]] * int(line[1:]) for line in input.split("\n") if line]

def solve_part1(rotations: [int]) -> int:
    position = initial_position
    num_exact_zeroes = 0

    for rotation in rotations:
        position += rotation
        position %= 100
        if position == 0:
            num_exact_zeroes += 1

    return num_exact_zeroes

def solve_part2(rotations: [int]) -> int:
    position = initial_position
    num_click_zeroes = 0
    
    for rotation in rotations:
        # Move one step at a time (brute force is fine)
        for _ in range(abs(rotation)):
            position += 1 if rotation > 0 else -1
            position %= 100
            if position == 0:
                num_click_zeroes += 1
    
    return num_click_zeroes

if __name__ == "__main__":
    with open("day01/input.txt", "r") as file:
        rotations = parse_input(file.read())

    print("Part 1: ", solve_part1(rotations))

    print("Part 2: ", solve_part2(rotations))