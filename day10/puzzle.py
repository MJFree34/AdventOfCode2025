from fractions import Fraction
from itertools import product

class Machine:
    def __init__(self, target_lights, buttons, joltage_reqs):
        self.target_lights = target_lights
        self.buttons = buttons
        self.joltage_reqs = joltage_reqs

def print_grid(grid):
    for row in grid:
        print(*row, sep='')

def parse_input(input):
    machines = []

    for line in input.split('\n'):
        target_lights_str = list(line[1:line.index(']')])
        target_lights = [1 if c == '#' else 0 for c in target_lights_str]
        line = line[line.index(']') + 2:]

        joltage_reqs_str = line[line.index('{') + 1:-1].split(',')
        joltage_reqs = [int(s) for s in joltage_reqs_str]
        line = line[:line.index('{') - 1]

        button_strs = line.split(' ')
        buttons = [[0 for _ in range(len(button_strs))] for _ in range(len(target_lights))]
        for i, button in enumerate(button_strs):
            indices = button[1:-1].split(',')
            for index in indices:
                buttons[int(index)][i] = 1


        machines.append(Machine(target_lights, buttons, joltage_reqs))

    return machines

def solve_part1(machines):
    sum_min_button_presses = 0

    for machine in machines:
        # print(f"Solving machine with target lights: {(''.join(map(str, machine.target_lights)))}")
        # print(f'Buttons:')
        # print_grid(machine.buttons)

        n = len(machine.target_lights)
        m = len(machine.buttons[0])

        augmented = [machine.buttons[i][:] + [machine.target_lights[i]] for i in range(n)]
        # print(f'Augmented matrix:')
        # print_grid(augmented)

        pivot_row = 0
        pivot_cols = []

        for col in range(m):
            found = False
            for row in range(pivot_row, n):
                if augmented[row][col] == 1:
                    augmented[pivot_row], augmented[row] = augmented[row], augmented[pivot_row]
                    found = True
                    break

            if not found:
                continue

            pivot_cols.append(col)
            
            # print(f'After finding pivot in column {col} at row {pivot_row}:')
            # print_grid(augmented)

            # Eliminate other rows that have a 1 in this column
            for row in range(n):
                if row != pivot_row and augmented[row][col] == 1:
                    for c in range(m + 1):
                        augmented[row][c] ^= augmented[pivot_row][c]
            
            # print(f'After elimination:')
            # print_grid(augmented)

            pivot_row += 1

        # print(f'Row echelon form:')
        # print_grid(augmented)

        # Check for impossible constraint
        for row in range(pivot_row, n):
            if all(augmented[row][c] == 0 for c in range(m)) and augmented[row][m] == 1:
                print('No solution exists for this machine.')
                return None

        # Find free variables (columns without pivots)
        free_vars = [col for col in range(m) if col not in pivot_cols]
        # print(f'Pivot columns: {pivot_cols}')
        # print(f'Free variables (buttons): {free_vars}')

        # Try all combinations of free variables
        min_button_presses = float('inf')
        best_solution = None

        for combo in range(2 ** len(free_vars)):
            # Set free variables according to this combination
            solution = [0] * m
            for i, free_var in enumerate(free_vars):
                solution[free_var] = (combo >> i) & 1

            # Back substitute to find pivot variable values
            for i in range(len(pivot_cols) - 1, -1, -1):
                col = pivot_cols[i]
                # solution[col] = augmented[i][m] XOR (sum of all later variables that affect this row)
                val = augmented[i][m]
                for j in range(col + 1, m):
                    if augmented[i][j] == 1:
                        val ^= solution[j]
                solution[col] = val

            # Check if this solution is better
            button_presses = sum(solution)
            if button_presses < min_button_presses:
                min_button_presses = button_presses
                best_solution = solution

        sum_min_button_presses += min_button_presses
        # print(f'Best solution: {best_solution}')
        # print(f'Minimum button presses: {min_button_presses}')
        # print("----------------------------")

    return sum_min_button_presses

# Used Gemini to help with this part. Multiple naive solutions were not working.
def solve_part2(machines):
    sum_min_button_presses = 0

    for machine in machines:
        n = len(machine.target_lights)
        m = len(machine.buttons[0])
        
        # Use Fraction for exact precision
        augmented = []
        for i in range(n):
            row = [Fraction(x, 1) for x in machine.buttons[i]]
            row.append(Fraction(machine.joltage_reqs[i], 1))
            augmented.append(row)

        pivot_row = 0
        pivot_cols = []
        
        # 1. Gaussian Elimination (Exact)
        for col in range(m):
            if pivot_row >= n: break

            pivot_idx = -1
            for row in range(pivot_row, n):
                if augmented[row][col] != 0:
                    pivot_idx = row
                    break
            
            if pivot_idx == -1: continue

            # Swap
            augmented[pivot_row], augmented[pivot_idx] = augmented[pivot_idx], augmented[pivot_row]
            pivot_cols.append(col)

            # Normalize
            pivot_val = augmented[pivot_row][col]
            for c in range(col, m + 1):
                augmented[pivot_row][c] /= pivot_val

            # Eliminate
            for row in range(n):
                if row != pivot_row and augmented[row][col] != 0:
                    factor = augmented[row][col]
                    for c in range(col, m + 1):
                        augmented[row][c] -= factor * augmented[pivot_row][c]
            
            pivot_row += 1

        # 2. Check Consistency
        possible = True
        for row in range(pivot_row, n):
            if augmented[row][m] != 0:
                possible = False
                break
        if not possible:
            continue # Impossible machine

        # 3. Solve for Free Variables
        free_vars = [col for col in range(m) if col not in pivot_cols]
        
        # If no free variables, just check the single solution
        if not free_vars:
            valid = True
            presses = 0
            for i, col in enumerate(pivot_cols):
                val = augmented[i][m]
                if val < 0 or val.denominator != 1:
                    valid = False
                    break
                presses += int(val)
            if valid:
                sum_min_button_presses += presses
                print(f"Solved determined machine. Presses: {presses}")
            continue
        
        best_total = float('inf')
        search_limit = 5000 
        
        # Optimization: If we have many free vars, reduce range
        if len(free_vars) > 2: search_limit = 200

        for free_vals in product(range(search_limit), repeat=len(free_vars)):
            current_free_sum = sum(free_vals)
            if current_free_sum >= best_total:
                continue

            solution = [Fraction(0, 1)] * m
            for i, f_idx in enumerate(free_vars):
                solution[f_idx] = Fraction(free_vals[i], 1)
            
            valid_solution = True
            current_total = current_free_sum
            
            # Back-solve
            for i in range(len(pivot_cols) - 1, -1, -1):
                col = pivot_cols[i]
                row_idx = i
                
                # val = Constant - Sum(Coeff * Free)
                val = augmented[row_idx][m]
                for f_idx in free_vars:
                    # Only cols to the right affect this pivot in RREF
                    if f_idx > col: 
                        val -= augmented[row_idx][f_idx] * solution[f_idx]
                
                # Check Integer and Non-Negative
                if val < 0 or val.denominator != 1:
                    valid_solution = False
                    break
                
                solution[col] = val
                current_total += int(val)
                
                # Pruning
                if current_total >= best_total:
                    valid_solution = False
                    break
            
            if valid_solution:
                best_total = current_total

        if best_total != float('inf'):
            sum_min_button_presses += best_total
            print(f"Solved machine. Min presses: {best_total}")
        else:
            print(f"No integer solution found in range {search_limit}.")

    return sum_min_button_presses

if __name__ == "__main__":
    with open("day10/input.txt", "r") as file:
        machines = parse_input(file.read())
 
    print("Part 1:", solve_part1(machines))

    print("Part 2:", solve_part2(machines))