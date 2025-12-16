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

def solve_part2(input):
    inv_id_sum = 0

    for r in input:
        lower = r['lower']
        upper = r['upper']

        # print(f"[{lower},{upper}]")

        # Use a set to prevent double counting inventory IDs
        inv_ids = set()

        for i in range(lower, upper + 1):
            num_str = str(i)
            num_len = len(num_str)

            # Skip single-digit inventory IDs
            if num_len == 1:
                continue

            for length in range(1, num_len + 1):
                # Skip inventory IDs that are not divisible by the current length
                if len(str(i)) % length != 0:
                    continue

                # Skip if this would create only 1 segment (the number itself)
                num_segments = num_len // length
                if num_segments == 1:
                    continue

                segments = [num_str[j:j+length] for j in range(0, num_len, length)]
                
                if len(set(segments)) == 1:
                    # print(f"      Invalid inventory ID found: {i} (segments: {segments})")
                    inv_ids.add(i)
                    break

        inv_id_sum += sum(inv_ids)

    return inv_id_sum

if __name__ == "__main__":
    with open("day02/input.txt", "r") as file:
        input = parse_input(file.read())

    print("Part 1: ", solve_part1(input))

    print("Part 2: ", solve_part2(input))

    # test1 = parse_input("99-1111")
    # test2 = parse_input("9-11")
    # test3 = parse_input("1-1000")
    # test4 = parse_input("100000-100001")
    # test5 = parse_input("111111-111111")

    # print("Test 1 Part 2: ", solve_part2(test1))
    # print("Test 2 Part 2: ", solve_part2(test2))
    # print("Test 3 Part 2: ", solve_part2(test3))
    # print("Test 4 Part 2: ", solve_part2(test4))
    # print("Test 5 Part 2: ", solve_part2(test5))