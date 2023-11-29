from sys import stdin

N = 10

rope = [(0, 0)] * N
ts = {(0, 0)}
loi, hii, loj, hij = [0, 0, 0, 0]
ls = list(stdin)
doprint = len(ls) < 15
doprint = False


def pprint():
    global loi, hii, loj, hij, doprint
    if not doprint:
        return
    n = hii - loi + 1
    m = hij - loj + 1
    if n > 6 or m > 6:
        return
    g = [['.'] * m for _ in range(n)]
    # print(loi, hii, loj, hij, n, m)
    g[-loi][-loj] = 's'
    for k in range(N - 1, -1, -1):
        g[rope[k][0] - loi][rope[k][1] - loj] = str(k) if k else 'H'
    print('\n'.join(''.join(r) for r in g))
    print()


def ns(si, sj):
    return {(i, j)
            for i in range(si - 1, si + 2) for j in range(sj - 1, sj + 2)}


def step(di, dj):
    global h, t, loi, hii, loj, hij, doprint
    rope[0] = (rope[0][0] + di, rope[0][1] + dj)
    loi = min(loi, rope[0][0])
    hii = max(hii, rope[0][0])
    loj = min(loj, rope[0][1])
    hij = max(hij, rope[0][1])
    for k in range(1, N):
        # print(rope[i - 1])
        hns = ns(*(rope[k - 1]))
        if rope[k] in hns:
            if doprint:
                print('stop at', k)
            return
        poss = ns(*rope[k]) & hns
        if len(poss) == 1:
            rope[k] = poss.pop()
        else:
            for i, j in poss:
                if i == rope[k - 1][0] or j == rope[k - 1][1]:
                    rope[k] = (i, j)
                    break
        if doprint:
            print('move', k, 'to', rope[k])
    ts.add(rope[-1])


for l in ls:
    d, k = l.split()
    d = {'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0)}[d]
    for _ in range(int(k)):
        step(d[0], d[1])
        pprint()

print(len(ts))