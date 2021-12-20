from sys import stdin
import functools as fntls
import operator as op

INF = float('inf')


def solve():
    isseat = [list(map(fntls.partial(op.eq, 'L'), l)) for l in lines()]
    h, w = len(isseat), len(isseat[0])
    seats = {(i,j) for i, r in enumerate(isseat) for j, v in enumerate(r) if v}
    occupied = set()

    prevoccupied = {1}
    while occupied != prevoccupied:
        prevoccupied = occupied
        occupied = set()
        for c in seats:
            i,j = c
            nc = sum(nc in prevoccupied for nc in neigh8(i,j,len(isseat), len(isseat[0])))
            if (c in prevoccupied and nc < 4) or (c not in prevoccupied and nc == 0):
                occupied.add(c)

    print(len(occupied))



def lines():
    return stdin.read().strip().split('\n')


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
