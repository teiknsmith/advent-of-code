from abc import abstractproperty
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


def solve():
    g =[[int(v) for v in r] for r in lines()]
    tot = 0
    for stepnum in range(1000000):
        flashed = set()
        for i, r in enumerate(g):
            for j, c in enumerate(r):
                g[i][j] = c + 1
                if c >= 9:
                    toflash = deque([(i,j)])
                    while toflash:
                        si, sj = toflash.popleft()
                        if (si,sj) in flashed:
                            continue
                        flashed.add((si, sj))
                        for oi, oj in neigh8(si,sj,len(g), len(g[0])):
                            g[oi][oj] += 1
                            if g[oi][oj] > 9:
                                toflash.append((oi, oj))
        for i,j in flashed:
            g[i][j] = 0
        if len(flashed) == len(g) * len(g[0]):
            print(stepnum + 1)
            break
        tot += len(flashed)
    # print(tot)

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
