from sys import stdin
from collections import defaultdict
import re

FIELDS = {
    "byr": re.compile(r"19[2-9]\d|200[0-2]"),
    "iyr": re.compile(r"20(1\d|20)"),
    "eyr": re.compile(r"20(2\d|30)"),
    "hgt": re.compile(r"1([5-8]\d|9[0-3])cm|(59|6\d|7[0-6])in"),
    "hcl": re.compile(r"#[0-9a-f]{6}"),
    "ecl": re.compile(r"amb|blu|brn|gry|grn|hzl|oth"),
    "pid": re.compile(r"\d{9}"),
    # "cid": re.compile(r".*"),
}


def valid(g):
    pp = defaultdict(lambda: "", (f.split(':') for f in ' '.join(g).split()))
    return all(patt.fullmatch(pp[f]) for f, patt in FIELDS.items())


def solve():
    print(sum(map(valid, groups())))


def groups():
    return [g.split('\n') for g in stdin.read().strip().split('\n\n')]


if __name__ == '__main__':
    solve()
