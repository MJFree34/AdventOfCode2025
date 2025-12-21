def parse_input(input):
    return [list(line) for line in input.split('\n')]

# def print_grid(grid):
#     for row in grid:
#         print(''.join(row))

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

if __name__ == "__main__":
    with open("day07/input.txt", "r") as file:
        input = parse_input(file.read())
 
    print("Part 1:", solve_part1(input))