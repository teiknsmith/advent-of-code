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
    sc = 0
    ch = {
        '[':']',
        '{':'}',
        '(':')',
        '<':'>'    }
    scmap = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }
    tocmp = []
    for l in lines():
        s = []
        for c in l:
            if c in ch:
                s.append(c)
            else:
                if c != ch[s[-1]]:
                    sc += scmap[c]
                    break
                s.pop()
        else:
            tocmp.append(s)
    
    print(sc)

    newscs = []
    for compsstck in tocmp:
        locsc = 0
        for c in reversed(compsstck):
            locsc*=5
            locsc += " ([{<".index(c)
        newscs.append(locsc)
    newscs.sort()
    print(newscs[len(newscs)//2])
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
