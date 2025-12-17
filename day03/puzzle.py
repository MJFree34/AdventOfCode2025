def parse_input(input):
    return [bank for bank in input.split('\n')]

def solve_part1(input):
    tot_out_joltage = 0

    for bank in input:
        first_max_value = max(bank)
        first_max_index = bank.index(first_max_value)

        if first_max_index == len(bank) - 1:
            second_max_value = first_max_value
            first_max_value = max(bank[:first_max_index])
        else:
            second_max_value = max(bank[first_max_index + 1:])

        # print(f"Bank: {bank}, Max: {first_max_value}, Second Max: {second_max_value}")

        tot_out_joltage += int(str(f"{first_max_value}{second_max_value}"))

    return tot_out_joltage

if __name__ == "__main__":
    with open("day03/input.txt", "r") as file:
        input = parse_input(file.read())

    print("Part 1:", solve_part1(input))