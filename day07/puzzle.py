def parse_input(input):
    return [list(line) for line in input.split('\n')]

# def print_grid(grid):
#     for row in grid:
#         print(''.join(str(row)))

def solve_part1(grid):
    # print("---Initial---")
    # print_grid(grid)

    tot_splits = 0
    beam_locs = {grid[0].index('S')}

    for row in grid[1:]:
        new_beam_locs = set()
        for loc in beam_locs:
            if row[loc] == '.':
                row[loc] = '|'
                new_beam_locs.add(loc)
            elif row[loc] == '^':
                if loc > 0:
                    row[loc - 1] = '|'
                    new_beam_locs.add(loc - 1)
                if loc < len(row) - 1:
                    row[loc + 1] = '|'
                    new_beam_locs.add(loc + 1)
                tot_splits += 1
        beam_locs = new_beam_locs

    # print("---Final---")
    # print_grid(grid)

    return tot_splits

def solve_part2(grid):
    timeline_grid = [[0 for _c in row] for row in grid]

    # Initialize bottom row with 1's
    for j, c in enumerate(grid[-1]):
        if c == '|':
            timeline_grid[-1][j] = 1

    for i in reversed(range(len(grid) - 1)):
        # Propogate beams upwards
        for j, c in enumerate(grid[i]):
            if c == '|' or c == 'S':
                timeline_grid[i][j] = timeline_grid[i + 1][j]

        # Calculate splitters
        for j, c in enumerate(grid[i]):
            if c == '^':
                left_count = timeline_grid[i + 1][j - 1] if j > 0 else 0
                right_count = timeline_grid[i + 1][j + 1] if j < len(grid[i]) - 1 else 0
                timeline_grid[i][j] = left_count + right_count
    
    # print_grid(timeline_grid)

    return timeline_grid[0][grid[0].index('S')]

if __name__ == "__main__":
    with open("day07/input.txt", "r") as file:
        input = parse_input(file.read())
 
    print("Part 1:", solve_part1(input))

    print("Part 2:", solve_part2(input))