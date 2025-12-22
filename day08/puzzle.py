import heapq
import math

NUM_PAIRS = 1000

class UnionFind:
    def __init__(self, points):
        self.parent = {p: p for p in points}
        self.size = {p: 1 for p in points}
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x != root_y:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]

    def get_all_sizes(self):
        roots = set(self.find(p) for p in self.parent)
        return {root: self.size[root] for root in roots}

def parse_input(input):
    return [tuple(int(x) for x in coord.split(',')) for coord in input.split('\n')]

def solve_part1(coords):
    min_heap = []

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            # Push (distance, index1, index2) to the heap
            heapq.heappush(min_heap, (math.dist(coords[i], coords[j]), i, j))

    uf = UnionFind(range(len(coords)))

    for _ in range(NUM_PAIRS):
        dist, i, j = heapq.heappop(min_heap)

        # print(f"Connecting points {coords[i]} and {coords[j]} with distance {dist}")
        uf.union(i, j)

    sorted_sizes = sorted(uf.get_all_sizes().values(), reverse=True)
    # print("Sorted sizes:", sorted_sizes)

    return sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]

def solve_part2(coords):
    min_heap = []

    for i in range(len(coords)):
        for j in range(i + 1, len(coords)):
            # Push (distance, index1, index2) to the heap
            heapq.heappush(min_heap, (math.dist(coords[i], coords[j]), i, j))

    uf = UnionFind(range(len(coords)))
    iterations = 0
    last_point_indices = (-1, -1)

    while iterations < NUM_PAIRS or len(uf.get_all_sizes()) > 1:
        dist, i, j = heapq.heappop(min_heap)

        # print(f"Connecting points {coords[i]} and {coords[j]} with distance {dist}")
        uf.union(i, j)
        iterations += 1
        last_point_indices = (i, j)

    return coords[last_point_indices[0]][0] * coords[last_point_indices[1]][0]

if __name__ == "__main__":
    with open("day08/input.txt", "r") as file:
        input = parse_input(file.read())
 
    print("Part 1:", solve_part1(input))

    print("Part 2:", solve_part2(input))