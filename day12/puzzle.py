from aocd import get_data, submit
from aocp import DictParser, ListParser, TupleParser
from dataclasses import dataclass

sample_input = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""

DEBUG_SEARCH = False


@dataclass
class Orientation:
    width: int
    height: int
    mask: int
    cells: tuple[tuple[int, int], ...]


@dataclass
class Shape:
    height: int
    width: int
    area: int
    orientations: list[Orientation]

    def __str__(self):
        orientations_bin = [
            {
                "width": orientation.width,
                "height": orientation.height,
                "mask": bin(orientation.mask),
            }
            for orientation in self.orientations
        ]
        return f"Shape(height={self.height}, width={self.width}, orientations={orientations_bin})"

    def __repr__(self):
        return self.__str__()


@dataclass
class Region:
    width: int
    length: int
    counts: list[int]


def bit_pos(x, y, width, height):
    return (height - y - 1) * width + (width - x - 1)


def bitmask_from_shape_str(shape_str):
    bitmask = 0
    lines = shape_str.split("\n")
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char == "#":
                bitmask |= 1 << bit_pos(x, y, len(line), len(lines))
    return bitmask


def mask_to_cells(mask, width, height):
    cells = []
    for y in range(height):
        for x in range(width):
            if mask & (1 << bit_pos(x, y, width, height)):
                cells.append((x, y))
    return tuple(cells)


def rotate_90(mask, height, width):
    new_mask = 0
    for y in range(height):
        for x in range(width):
            if mask & (1 << (y * width + x)):
                new_x = height - 1 - y
                new_y = x
                new_mask |= 1 << (new_y * height + new_x)
    return new_mask


def mirror_horizontal(mask, height, width):
    new_mask = 0
    for y in range(height):
        for x in range(width):
            if mask & (1 << (y * width + x)):
                new_x = width - 1 - x
                new_mask |= 1 << (y * width + new_x)
    return new_mask


def calc_orientations(height, width, shape_str):
    seen = set()
    orientations = []

    def add_orientation(mask, o_width, o_height):
        key = (mask, o_width, o_height)
        if key not in seen:
            seen.add(key)
            orientations.append(
                Orientation(
                    width=o_width,
                    height=o_height,
                    mask=mask,
                    cells=mask_to_cells(mask, o_width, o_height),
                )
            )

    start_mask = bitmask_from_shape_str(shape_str)
    cur_mask = start_mask
    cur_width = width
    cur_height = height
    for _ in range(4):
        add_orientation(cur_mask, cur_width, cur_height)
        cur_mask = rotate_90(cur_mask, cur_height, cur_width)
        cur_width, cur_height = cur_height, cur_width

    cur_mask = mirror_horizontal(start_mask, height, width)
    cur_width = width
    cur_height = height
    for _ in range(4):
        add_orientation(cur_mask, cur_width, cur_height)
        cur_mask = rotate_90(cur_mask, cur_height, cur_width)
        cur_width, cur_height = cur_height, cur_width

    return orientations


def create_shape_from_rows(shape_rows):
    height = len(shape_rows)
    width = len(shape_rows[0]) if shape_rows else 0
    shape_str = "\n".join(shape_rows)
    return Shape(
        height=height,
        width=width,
        area=sum(row.count("#") for row in shape_rows),
        orientations=calc_orientations(height, width, shape_str),
    )


def parse_input(raw_data):
    block_parser = ListParser(splitter="\n\n")
    line_parser = ListParser(splitter="\n")
    blocks_raw = block_parser.parse(raw_data.strip())
    shape_blocks = []
    region_lines = []

    for block in blocks_raw:
        block_lines = line_parser.parse(block.strip())
        first_line = block_lines[0]
        if "x" in first_line and ": " in first_line:
            region_lines.extend(block_lines)
        else:
            shape_blocks.append(block)

    shape_parser = DictParser(
        value_parser=ListParser(splitter="\n"),
        sequence_splitter="\n\n",
        key_value_splitter=":\n",
    )
    shape_parser.tuple_parser = TupleParser(
        subparser=[int, ListParser(splitter="\n")],
        splitter=":\n",
    )
    shape_strs = shape_parser.parse("\n\n".join(shape_blocks))
    shapes = [create_shape_from_rows(shape_rows) for shape_rows in shape_strs.values()]

    size_parser = TupleParser(subparser=[int, int], splitter="x")
    count_parser = ListParser(subparser=int, splitter=" ")
    region_parser = TupleParser(subparser=[size_parser, count_parser], splitter=": ")
    regions_raw = ListParser(subparser=region_parser, splitter="\n").parse(
        "\n".join(region_lines)
    )
    regions = [
        Region(width=width, length=length, counts=counts)
        for (width, length), counts in regions_raw
    ]

    expected_count_len = len(shapes)
    for region in regions:
        if len(region.counts) != expected_count_len:
            raise ValueError(
                "Region count vector length does not match shape count: "
                f"{len(region.counts)} != {expected_count_len}"
            )

    return shapes, regions


def placement_mask(region, orientation, left, top):
    placed = 0
    for cell_x, cell_y in orientation.cells:
        board_x = left + cell_x
        board_y = top + cell_y
        if (
            board_x < 0
            or board_y < 0
            or board_x >= region.width
            or board_y >= region.length
        ):
            return None
        placed |= 1 << bit_pos(board_x, board_y, region.width, region.length)
    return placed


def precompute_placements(shapes, region):
    """For each shape, compute all valid board masks for this region."""
    placements = []
    for shape in shapes:
        shape_placements = []
        for orientation in shape.orientations:
            for left in range(region.width - orientation.width + 1):
                for top in range(region.length - orientation.height + 1):
                    placed = placement_mask(region, orientation, left, top)
                    if placed is not None:
                        shape_placements.append(placed)
        # Deduplicate: symmetric orientations can produce identical masks
        placements.append(list(dict.fromkeys(shape_placements)))
    return placements


def has_valid_tiling(shapes, region, counts):
    total_bits = region.width * region.length

    # Precompute all valid placements per shape for this region
    all_placements = precompute_placements(shapes, region)

    # Quick area feasibility check before searching
    required_cells = sum(c * shapes[i].area for i, c in enumerate(counts))
    if required_cells > total_bits:
        return False

    memo = {}

    def search(board, remaining):
        # All pieces placed - success. Grid does NOT need to be fully covered.
        if all(c == 0 for c in remaining):
            return True

        state_key = (board, tuple(remaining))
        if state_key in memo:
            return memo[state_key]

        # Area prune: not enough free space left for remaining pieces
        free_cells = total_bits - board.bit_count()
        required = sum(c * shapes[i].area for i, c in enumerate(remaining))
        if required > free_cells:
            memo[state_key] = False
            return False

        # MRV heuristic: pick the shape type with the fewest valid placements
        # on the current board (most constrained variable first)
        best_shape_idx = None
        best_valid_count = None
        for i, count in enumerate(remaining):
            if count == 0:
                continue
            valid = sum(1 for pm in all_placements[i] if not (board & pm))
            if best_valid_count is None or valid < best_valid_count:
                best_valid_count = valid
                best_shape_idx = i

        # No valid placement exists for the most constrained shape - dead end
        if best_shape_idx is None or best_valid_count == 0:
            memo[state_key] = False
            return False

        # Try all valid placements for the chosen shape
        shape_idx = best_shape_idx
        remaining[shape_idx] -= 1
        result = False
        for placed in all_placements[shape_idx]:
            if board & placed:
                continue
            if search(board | placed, remaining):
                result = True
                break
        remaining[shape_idx] += 1

        memo[state_key] = result
        return result

    return search(0, counts[:])


def solve_part1(shapes, regions):
    total = 0
    for idx, region in enumerate(regions):
        if DEBUG_SEARCH:
            print(
                f"\n=== Region {idx} ({region.width}x{region.length}) counts={region.counts} ==="
            )
        if has_valid_tiling(shapes, region, region.counts[:]):
            total += 1
    return total


if __name__ == "__main__":
    raw_data = get_data(day=12, year=2025)
    # raw_data = sample_input.strip()
    shapes, regions = parse_input(raw_data)
    submit(solve_part1(shapes, regions), part="a", day=12, year=2025)
