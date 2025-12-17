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

def solve_part2(input):
    tot_out_joltage = 0

    for bank in input:
        to_drop = len(bank) - 12
        stack = []

        for digit in bank:
            while stack and to_drop > 0 and stack[-1] < digit:
                stack.pop()
                to_drop -= 1
            stack.append(digit)

        result = ''.join(stack[:12])

        # print(f"Bank: {bank}, Top 12: {result}")

        tot_out_joltage += int(result)

    return tot_out_joltage

if __name__ == "__main__":
    with open("day03/input.txt", "r") as file:
        input = parse_input(file.read())

    print("Part 1:", solve_part1(input))

    print("Part 2:", solve_part2(input))