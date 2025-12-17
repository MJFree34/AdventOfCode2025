def parse_input(input):
    return [list(row) for row in input.split('\n')]

def solve_part1(input):
    # output_grid = ''

    num_reachable_rolls = 0

    for i in range(len(input)):
        for j in range(len(input[i])):
            num_adjacent_rolls = 0
            
            if input[i][j] == '@':
                for (di, dj) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < len(input) and 0 <= nj < len(input[i]):
                        if input[ni][nj] == '@':
                            num_adjacent_rolls += 1
            
                if num_adjacent_rolls < 4:
                    num_reachable_rolls += 1
                    # output_grid += 'x'
                # else:
                #     output_grid += input[i][j]
            # else:
            #     output_grid += input[i][j]
        # output_grid += '\n'

    # print(output_grid)
    return num_reachable_rolls

def solve_part2(input):
    num_reachable_rolls = 0
    iteration = 0

    while True:
        # print(f"Iteration {iteration}")
        iter_reachable_rolls = 0
        output_grid = ''

        for i in range(len(input)):
            for j in range(len(input[i])):
                num_adjacent_rolls = 0
                
                if input[i][j] == '@':
                    for (di, dj) in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                        ni, nj = i + di, j + dj
                        if 0 <= ni < len(input) and 0 <= nj < len(input[i]):
                            if input[ni][nj] == '@':
                                num_adjacent_rolls += 1
                
                    if num_adjacent_rolls < 4:
                        iter_reachable_rolls += 1
                        output_grid += 'x'
                    else:
                        output_grid += '@'
                else:
                    output_grid += '.'
            output_grid += '\n'

        num_reachable_rolls += iter_reachable_rolls
        iteration += 1
        input = parse_input(output_grid.strip())

        # print("Reachable rolls this iteration:", iter_reachable_rolls)
        # print(output_grid)
        # print("----------------------------------------")

        if iter_reachable_rolls == 0:
            break

    return num_reachable_rolls

if __name__ == "__main__":
    with open("day04/input.txt", "r") as file:
        input = parse_input(file.read())

    print("Part 1:", solve_part1(input))

    print("Part 2:", solve_part2(input))