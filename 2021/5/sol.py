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
    ls = []
    for l in lines():
        a, b = l.split(' -> ')
        i1, j1 = map(int, a.split(','))
        i2, j2 = map(int, b.split(','))
        ls.append((i1, j1, i2, j2))
    n = max(max(l) for l in ls) + 1
    floor = [[0] * n for _ in range(n)]

    for l in ls:
        i1, j1, i2, j2 = l
        di = i2 - i1
        dj = j2 - j1
        # if di and dj:
        #     continue
        d = math.gcd(di, dj)
        stepi = di // d
        stepj = dj // d
        nstepsi = 0 if di == 0 else di // stepi
        nstepsj = 0 if dj == 0 else dj // stepj
        nsteps = max(nstepsi, nstepsj)
        for i, j in [(i1 + stepi * s, j1 + stepj * s)
                     for s in range(nsteps + 1)]:
            floor[j][i] += 1

    for r in floor:
        print(r)
    c = 0
    for i in range(n):
        for j in range(n):
            if floor[i][j] > 1:
                c += 1
    print(c)


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
