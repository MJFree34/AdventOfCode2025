from aocd import get_data, submit
from aocp import ListParser, TupleParser, DictParser
# from pprint import pprint

sample_input = """
aaa: you hhh
you: bbb ccc
bbb: ddd eee
ccc: ddd eee fff
ddd: ggg
eee: out
fff: out
ggg: out
hhh: ccc fff iii
iii: out
"""

def solve_part1(cables_dict):
    def dfs(cable_name, path):
        cables = cables_dict[cable_name]
        total = 0
        for conn in cables:
            current_path = path + [cable_name]
            if conn == "out":
                full_path = current_path + [conn]
                print("Found path:", " -> ".join(full_path))
                total += 1
                continue
            total += dfs(conn, current_path)
        return total

    total_paths = dfs("you", [])
    return total_paths

if __name__ == "__main__":
    raw_data = get_data(day=11, year=2025)
    # raw_data = sample_input.strip()

    value_list_parser = ListParser(splitter=" ")
    parser = DictParser(
        value_parser=value_list_parser,
        sequence_splitter="\n",
        key_value_splitter=": ",
    )
    parser.tuple_parser = TupleParser(
        subparser=[str, value_list_parser],
        splitter=":",
    )

    cables = parser.parse(raw_data)
    # pprint(cables)

    submit(solve_part1(cables), part="a", day=11, year=2025)