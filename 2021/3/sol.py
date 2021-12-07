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
    ls = lines()
    cs = [[0, 0] for _ in range(len(ls[0]))]
    for l in ls:
        for i, c in enumerate(l):
            cs[i][int(c)] += 1
    g = []
    e = []
    for z, o in cs:
        if z > o:
            g.append('1')
            e.append('0')
        else:
            e.append('1')
            g.append('0')
    print(int(''.join(g), base=2) * int(''.join(e), base=2))

    os = set(ls)
    co2s = set(ls)
    for i, (z, o) in enumerate(cs):
        newos = set()
        newc02s = set()
        counts = [0, 0]
        for s in os:
            counts[int(s[i])] += 1
        if counts[0] > counts[1]:
            ocheck = '1'
        elif counts[0] < counts[1]:
            ocheck = '0'
        else:
            ocheck = '0'
        counts = [0, 0]
        for s in co2s:
            counts[int(s[i])] += 1
        if counts[0] > counts[1]:
            ccheck = '0'
        elif counts[0] < counts[1]:
            ccheck = '1'
        else:
            ccheck = '1'

        if len(os) == 1:
            newos = os
        else:
            for s in os:
                if s[i] == ocheck:
                    newos.add(s)
        os = newos
        if len(co2s) == 1:
            newc02s = co2s
        else:
            for s in co2s:
                if s[i] == ccheck:
                    newc02s.add(s)
        co2s = newc02s

    print(int(co2s.pop(), base=2) * int(os.pop(), base=2))

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
