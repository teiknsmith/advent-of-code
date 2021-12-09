import numpy as np
from sys import float_info, stdin
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
    ls = lines()
    ls = [[int(c) for c in r] for r in ls]
    tot = 0
    floors = []
    for i, r in enumerate(ls):
        for j, c in enumerate(r):
            if all(ls[oi][oj] > ls[i][j] for oi, oj in neigh4(i,j,len(ls), len(r))):
                tot += c + 1
                floors.append((i,j))
    print(tot)
    cs = []
    for bi, (i,j) in enumerate(floors):
        tosee = deque()
        tosee.append((i, j))
    
        seen = set()
        c = 0
        while tosee:
            i, j = tosee.popleft()
            if (i,j) in seen:
                continue
            seen.add((i,j))
            if ls[i][j] == 9:
                continue
            for oi, oj in neigh4(i,j, len(ls), len(ls[0])):
                tosee.append((oi, oj))
            c += 1
        cs.append(c)
    a, b, c  = sorted(cs)[-3:]
    print(a*b*c)



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
