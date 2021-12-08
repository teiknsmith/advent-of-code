import numpy as np
from sys import stdin
from collections import deque as deq
from copy import copy
import functools as fntls
import itertools as ittls
import operator as op
import math
import re
import string
import heapq as q

e = enumerate
INF = float('inf')


def solve():
    digsofinterest = set([1, 4, 7, 8])
    digmap = {
        frozenset("abcefg"): 0,
        frozenset("cf"): 1,
        frozenset("acdeg"): 2,
        frozenset("acdfg"): 3,
        frozenset("bdcf"): 4,
        frozenset("abdfg"): 5,
        frozenset("abdefg"): 6,
        frozenset("acf"): 7,
        frozenset("abcdefg"): 8,
        frozenset("abcdfg"): 9,
    }
    c = 0
    tot = 0
    for l in lines():
        al, out = l.split('|')
        al = sorted(al.split(), key=len)
        print(al)
        al = [set(el) for el in al]
        mapping = {k: None for k in "abcdefg"}
        mapping['a'] = (al[1] - al[0]).pop()
        candf = al[1] - {mapping['a']}
        bandd = al[2] - candf
        for i in [3, 4, 5]:
            if bandd.issubset(al[i]):
                mapping['g'] = (
                    al[i] - (candf.union(bandd).union({mapping['a']}))).pop()
                break
        mapping['e'] = (al[-1] -
                        (bandd.union(candf).union(set(mapping[k]
                                                      for k in "ag")))).pop()

        for val in bandd:
            if all(val in al[i] for i in [3, 4, 5]):
                mapping['d'] = val
                mapping['b'] = (bandd - {val}).pop()
                break
        for val in candf:
            if sum(1 if val in al[i] else 0 for i in [6, 7, 8]) == 3:
                mapping['f'] = val
                mapping['c'] = (candf - {val}).pop()

        digs = []
        rmap = {v: k for k, v in mapping.items()}
        for lets in out.split():
            reallets = frozenset(rmap[l] for l in lets)
            digit = digmap[reallets]
            if digit in digsofinterest:
                c += 1
            digs.append(digit)
        tot += int(''.join(map(str, digs)))
    print(c)
    print(tot)

    pass


def lines():
    return stdin.read().strip().split('\n')


def groups():
    return [g.split('\n') for g in stdin.read().strip().split('\n\n')]


def btwn(v, l, h):
    return (v > l and v < h) or (v < l and v > h)


def btwne(v, l, h):
    return (v >= l and v <= h) or (v <= l and v >= h)


def btwni(v, l, h):
    return v >= l and v < h


def valids(ijl, hii, hij):
    for i, j in ijl:
        if (btwni(i, -INF if hii == INF else 0, hii)
                and btwni(j, -INF if hii == INF else 0, hij)):
            yield (i, j)


def neigh4(i, j, hii=INF, hij=INF):
    yield from valids([(i - 1, j), \
                        (i + 1, j), \
                        (i, j - 1), \
                        (i, j + 1)], hii, hij)


def neigh8(i, j, hii=INF, hij=INF):
    yield from neigh4(i, j, hii, hij)
    yield from valids([(i - 1, j - 1), \
                        (i - 1, j + 1), \
                        (i + 1, j - 1), \
                        (i + 1, j + 1)], hii, hij)


if __name__ == '__main__':
    solve()
