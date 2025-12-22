import heapq
import shapely
from shapely import Polygon

def parse_input(input):
    return [tuple(int(x) for x in coord.split(',')) for coord in input.split('\n')]

def print_grid(grid):
    for row in grid:
        print(''.join(row))

def solve_part1(coords):
    max_area = 0

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            width = abs(coords[i][0] - coords[j][0]) + 1
            height = abs(coords[i][1] - coords[j][1]) + 1
            area = width * height
            if area > max_area:
                max_area = area

    return max_area

def solve_part2(coords):
    area_full = Polygon(coords)
    areas = []

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            width = abs(coords[i][0] - coords[j][0]) + 1
            height = abs(coords[i][1] - coords[j][1]) + 1
            area = width * height
            heapq.heappush(areas, (-area, (i, j)))

    while areas:
        neg_area, (i, j) = heapq.heappop(areas)
        area_partial = Polygon(
            [
                (coords[i][0], coords[j][1]),
                (coords[j][0], coords[j][1]),
                (coords[j][0], coords[i][1]),
                (coords[i][0], coords[i][1])
            ]
        )
        if shapely.within(area_partial, area_full):
            return -neg_area

    return -1

if __name__ == "__main__":
    with open("day09/input.txt", "r") as file:
        input = parse_input(file.read())
 
    print("Part 1:", solve_part1(input))

    print("Part 2:", solve_part2(input))