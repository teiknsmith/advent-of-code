import numpy as np
from sys import stdin
from collections import defaultdict, deque
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
    es = defaultdict(lambda: set())
    for l in lines():
        u, v = l.split('-')
        es[u].add(v)
        es[v].add(u)
    paths = {k:set() for k in es}
    tovis = deque()
    tovis.append(('start', "", False))
    while tovis:
        u, p, hasdup = tovis.popleft()
        for v in es[u]:
            doprint = False
            if doprint:
                print(f"{p} going to {v}, {hasdup=}")
            if ((not hasdup) or (v.isupper() or v not in p)) and (v != "start"):
                if doprint:
                    print("   actually")
                newpath = p + f",{v}"
                # hasdup = hasdup or (v.islower() and (v in p))
                if v != 'end':
                    tovis.append((v, newpath, hasdup or (v.islower() and (v in p))))
                paths[v].add(newpath)
    print(len(paths['end']))
    # for p in sorted(paths['end']):
    #     if p == ",A,b,A,c,A,b,A,end":
    #         print(p)
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
