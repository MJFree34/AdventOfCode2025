import math

NUM_PAIRS = 10

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
    distances = [[0 for _ in range(len(coords))] for _ in range(len(coords))]

    for i in range(len(coords)):
        for j in range(len(coords)):
            if i != j:
                distances[i][j] = math.dist(coords[i], coords[j])

    uf = UnionFind(range(len(coords)))

    for _ in range(NUM_PAIRS):
        min_distance = distances[0][1]
        min_distance_indices = (0, 1)

        for i in range(len(coords)):
            for j in range(len(coords)):
                if i != j:
                    if distances[i][j] != 0 and distances[i][j] < min_distance:
                        min_distance = distances[i][j]
                        min_distance_indices = (i, j)
        # print(f"Connecting points {coords[min_distance_indices[0]]} and {coords[min_distance_indices[1]]} with distance {min_distance}")
        distances[min_distance_indices[0]][min_distance_indices[1]] = 0
        distances[min_distance_indices[1]][min_distance_indices[0]] = 0
        uf.union(min_distance_indices[0], min_distance_indices[1])

    sorted_sizes = sorted(uf.get_all_sizes().values(), reverse=True)
    # print("Sorted sizes:", sorted_sizes)

    return sorted_sizes[0] * sorted_sizes[1] * sorted_sizes[2]

if __name__ == "__main__":
    with open("day08/input.txt", "r") as file:
        input = parse_input(file.read())
 
    print("Part 1:", solve_part1(input))