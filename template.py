import numpy as np
from sys import stdin
from collections import deque, defaultdict
from copy import copy
import functools as fntls
import itertools as ittls
import operator as op
import math
import re
import string
import heapq as q

INF = float('inf')


def solve():
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
