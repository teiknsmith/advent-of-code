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
    g = [[0]*1000 for _ in range(1000)]
    for l in lines():
        if l.startswith("turn"):
            bits = l.split()
            newval = 1 if bits[1] == 'on' else -1
            i1,j1 = map(int, bits[2].split(','))
            i2,j2 = map(int, bits[4].split(','))
            for i in range(i1, i2+1):
                for j in range(j1, j2+1):
                    g[i][j] += newval
                    g[i][j] = max(g[i][j], 0)
        else:
            bits = l.split()
            i1,j1 = map(int, bits[1].split(','))
            i2,j2 = map(int, bits[3].split(','))
            for i in range(i1, i2+1):
                for j in range(j1, j2+1):
                    g[i][j] += 2#not g[i][j]
    c = 0
    for r in g:
        for v in r:
            if v:
                c+= v
    print(c)
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
