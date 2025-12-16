def parse_input(input):
    return [{'lower': int(range.split('-')[0]), 'upper': int(range.split('-')[1])} for range in input.split(',')]

def solve_part1(input):
    inv_id_sum = 0

    for r in input:
        lower = r['lower']
        upper = r['upper']

        # print(f"[{lower},{upper}]")

        for i in range(lower, upper + 1):
            # Skip odd-length inventory IDs
            if len(str(i)) % 2 != 0:
                continue
            first_half = str(i)[:len(str(i)) // 2]
            second_half = str(i)[len(str(i)) // 2:]
            # print(f"  {i}: {first_half} | {second_half}")

            if int(first_half) == int(second_half):
                # print(f"    Invalid inventory ID found: {i}")
                inv_id_sum += i

    return inv_id_sum

if __name__ == "__main__":
    with open("day02/input.txt", "r") as file:
        input = parse_input(file.read())

    print("Part 1: ", solve_part1(input))