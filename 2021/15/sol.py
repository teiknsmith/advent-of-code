from sys import stdin
import heapq as q

INF = float('inf')


def solve():
    g = intgridin()

    h = len(g)
    w = len(g[0])

    # uncomment the `*5`s for Part 2
    imax = h #* 5
    jmax = w #* 5

    def cellval(i, j):
        addi, gi = divmod(i, h)
        addj, gj = divmod(j, w)
        return (g[gi][gj] + addi + addj - 1)%9+1

    lowest = [[INF] * (jmax) for _ in range(imax)]
    lowest[0][0] = 0
    tosee = [(0, 0, 0)]
    seen = set()
    while tosee:
        d, i, j = q.heappop(tosee)
        if (i, j) in seen:
            continue
        seen.add((i, j))
        for oi, oj in neigh4(i, j, imax, jmax):
            if (oi, oj) in seen:
                continue
            newd = d + cellval(oi, oj)
            if newd < lowest[oi][oj]:
                lowest[oi][oj] = newd
                q.heappush(tosee, (newd, oi, oj))
    print(lowest[-1][-1])


def lines():
    return stdin.read().strip().split('\n')


def intgridin():
    return [[int(c) for c in r] for r in lines()]


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




if __name__ == '__main__':
    solve()
