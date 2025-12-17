from math import comb


def parse_input(input):
    ranges_str, ing_ids_str = input.split('\n\n')
    ranges = [[int(x) for x in range.split('-')] for range in ranges_str.splitlines()]
    ing_ids = [int(id_str) for id_str in ing_ids_str.splitlines()]
    return ranges, ing_ids

def combined_ranges(ranges):
    sorted_ranges = sorted(ranges, key=lambda r: r[0])
    combined = [sorted_ranges[0]]

    # print(f"Sorted Ranges: {sorted_ranges}")

    for r in sorted_ranges[1:]:
        last = combined[-1]

        # Perform merging logic or append
        if r[0] <= last[1]:
            last[1] = max(last[1], r[1])
        else:
            combined.append(r)
    
    return combined

def solve_part1(fresh_ids, ing_ids):
    tot_fresh_ids = 0

    for ing_id in ing_ids:
        for fr in fresh_ids:
            if fr[0] <= ing_id <= fr[1]:
                tot_fresh_ids += 1
                break

    return tot_fresh_ids

if __name__ == "__main__":
    with open("day05/input.txt", "r") as file:
        ranges, ing_ids = parse_input(file.read())

    combined_ranges = combined_ranges(ranges)

    print("Part 1:", solve_part1(combined_ranges, ing_ids))