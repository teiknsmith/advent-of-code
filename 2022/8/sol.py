from sys import stdin
from functools import *
from operator import *

g = [list(map(int, r)) for r in stdin.read().strip().split('\n')]
n, m = len(g), len(g[0])


def score1(i, j, di, dj):
    doprint = (i, j) == (3, 2)
    doprint = False
    if doprint:
        print(i, j, di, dj, end=' -> ')
    h = g[i][j]
    r = 0
    i += di
    j += dj
    while 0 <= i < n and 0 <= j < m:
        r += 1
        if g[i][j] >= h:
            break
        i += di
        j += dj
    if doprint:
        print(r)
    return r


def score(i, j):
    return reduce(mul, (score1(i, j, di, dj)
                        for di, dj in ((-1, 0), (1, 0), (0, 1), (0, -1))))


vis = [[False] * m for _ in range(n)]
for i in range(n):
    p = -1
    for j in range(m):
        if g[i][j] > p:
            vis[i][j] = True
        p = max(p, g[i][j])
    p = -1
    for j in range(m - 1, -1, -1):
        if g[i][j] > p:
            vis[i][j] = True
        p = max(p, g[i][j])
for j in range(m):
    p = -1
    for i in range(n):
        if g[i][j] > p:
            vis[i][j] = True
        p = max(p, g[i][j])
    p = -1
    for i in range(n - 1, -1, -1):
        if g[i][j] > p:
            vis[i][j] = True
        p = max(p, g[i][j])

print(sum(sum(r) for r in vis))

scs = [[score(i, j) for j in range(m)] for i in range(n)]
# {*map(print, g)}
# print()
# {*map(print, scs)}
print(max(max(r) for r in scs))