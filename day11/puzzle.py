from aocd import get_data, submit
from aocp import ListParser, TupleParser, DictParser
from functools import cache
from pprint import pprint

# Credit: https://www.reddit.com/user/4HbQ/ for solution

sample_input1 = """
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

sample_input2 = """
svr: aaa bbb
aaa: fft
fft: ccc
bbb: tty
tty: ccc
ccc: ddd eee
ddd: hub
hub: fff
eee: dac
dac: fff
fff: ggg hhh
ggg: out
hhh: out
"""

cables = {}

@cache
def count(here, dest):
    return here == dest or sum(count(next, dest) for next in cables[here])

def solve_part1():
    return count("you", "out")

def solve_part2():
    svr_dac_paths = count('svr', 'dac')
    svr_fft_paths = count('svr', 'fft')
    dac_fft_paths = count('dac', 'fft')
    fft_dac_paths = count('fft', 'dac')
    dac_out_paths = count('dac', 'out')
    fft_out_paths = count('fft', 'out')
    return svr_dac_paths * dac_fft_paths * fft_out_paths + svr_fft_paths * fft_dac_paths * dac_out_paths

if __name__ == "__main__":
    raw_data = get_data(day=11, year=2025)
    # raw_data = sample_input1.strip()
    # raw_data = sample_input2.strip()

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

    cables = parser.parse(raw_data) | {'out':[]}
    # pprint(cables)

    # print("Part 1:", solve_part1())
    # submit(solve_part1(), part="a", day=11, year=2025)

    # print("Part 2:", solve_part2())
    submit(solve_part2(), part="b", day=11, year=2025)