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

def scoreboard(boolboard, numboard):
    for g in [zip(range(5), [i]*5) for i in range(5)]+[zip([i]*5, range(5)) for i in range(5)]:#+[zip(range(5), range(5))]+[zip(range(5), range(4, -1,-1))]:
        if all(boolboard[i][j] for i,j in g):
            for r in numboard:
                print(r)
            print()
            return sum(int(numboard[i][j]) for i in range(5) for j in range(5) if not boolboard[i][j])
    return None
    pass
def solve():
    gs = groups()
    ns = gs[0][0].strip().split(',')
    print(ns)
    nlocs = {n: set() for n in ns}
    boards = []
    boardbools = []
    for boardi, g in enumerate(gs[1:]):
        # print(g)
        boards.append([r.strip().split() for r in g])
        for i in range(5):
            for j in range(5):
                s = boards[-1][i][j]
                # if s == '7':
                #     print('7 at ', boardi, i, j)
                nlocs[s].add((boardi, i, j))
        boardbools.append([[False]*5 for _ in range(5)])

    activeboards = set(range(len(boards)))
    done = False
    for n in ns:
        for b, i, j in nlocs[n]:
            if b not in activeboards:
                continue
            # print(n,b,i,j)
            board = boardbools[b]
            board[i][j] = True
            # if b == 0:
            #     for r in board:
            #         print(r)
            #     print()
            sc = scoreboard(board, boards[b])
            if sc:
                if len(activeboards) == 1:
                    print(sc*int(n))
                    done = True
                    break
                else:
                    activeboards.remove(b)
        if done:
            break
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
