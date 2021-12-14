from sys import stdin
from collections import defaultdict, Counter
import functools as fntls
import operator as op


def solve():
    ls = lines()

    rules = defaultdict(lambda: dict())
    for rule in ls[2:]:
        a, b = rule.split(' -> ')
        rules[a[0]][a[1]] = b

    @fntls.lru_cache(maxsize=None)
    def expand(c, nextc, n):
        res = Counter()
        if n == 0 or not (nextc in rules[c]):
            res[c] = 1
            return res

        midc = rules[c][nextc]
        counts1 = expand(c, midc, n - 1)
        counts2 = expand(midc, nextc, n - 1)
        return counts1 + counts2

    og_str = ls[0]
    n = 40
    counts = sorted(
        fntls.reduce(op.add, (expand(og_str[i], og_str[i + 1], n)
                              for i in range(len(og_str) - 1)),
                     Counter({og_str[-1]: 1})).values())

    print(counts[-1] - counts[0])


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
