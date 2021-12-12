from typing import Counter
import numpy as np
from sys import stdin
from collections import deque
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

def nice(l):
    cs = Counter(l)
    if sum(cs[k] for k in "aeiou") < 3:
        return False
    if any(bad in l for bad in "ab cd pq xy".split()):
        return False
    prev = l[0]
    for c in l[1:]:
        if c == prev:
            return True
        prev = c
    return False

def nice2(l):
    pairs = set()
    p = l[0]
    hasrep = False
    hasgap = False
    for c, n in zip(l[1:], l[2:]):
        if l == "zgsnvdmlfuplrubt":
            print(p, c,n)
        if (c,n) in pairs:
            if hasgap:
                return True
            hasrep = True
        if p == n:
            if hasrep:
                return True
            hasgap = True
        pairs.add((p,c))
        p  = c

    return False

def solve():
    print(len(list(l for l in lines() if nice2(l))))
    pass


def lines():
    return stdin.read().strip().split('\n')


def intgridin():
    return [[int(c) for c in r] for r in lines()]


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
