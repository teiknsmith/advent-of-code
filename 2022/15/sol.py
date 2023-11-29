from sys import stdin
import re

y, *ls = stdin.read().strip().split('\n')
y = int(y)

inp = []
for l in ls:
    sx, sy, bx, by = map(
        int,
        re.match(
            r"Sensor at x=(-?[^d]+), y=(-?[^d]+): closest beacon is at x=(-?[^d]+), y=(-?[^d]+)",
            l).groups())
    inp.append((sx, sy, bx, by))

ybeacxs = set()
evs = []
for sx, sy, bx, by in inp:
    if by == y:
        ybeacxs.add(bx)
    d = abs(sx - bx) + abs(sy - by)
    r = d - abs(sy - y)
    if r < 0:
        continue
    evs.append((sx - r, -1))
    evs.append((sx + r + 1, +1))

evs.sort()
cov = 0
r = 0
px = None
for x, d in evs:
    if d == -1 and cov == 0:
        px = x
    cov -= d
    if d == 1 and cov == 0:
        r += x - px
print(r - len(ybeacxs))

maxc = 2 * y

# def inters(a, b):
#     sx1, sy1, bx1, by1 = a
#     sx2, sy2, bx2, by2 = b
#     d1 = abs(sx1 - bx1) + abs(sy1 - by1)
#     d2 = abs(sx2 - bx2) + abs(sy2 - by2)
#     ds = abs(sx2 - sx2) + abs(sy2 - sy2)
#     if ds > d1 + d2 + 2:
#         # not touching
#         return []
#     if ds + min(d1, d2) <= max(d1, d2):
#         # fully enclosing
#         return []
#     if ds == d1 + d2 + 2:
#         return []
#     return [(0, 0)]

# def isin(coord, a):
#     sx, sy, bx, by = a
#     x, y = coord
#     sd = abs(sx - bx) + abs(sy - by)
#     pd = abs(sx - x) + abs(sy - y)
#     return pd <= sd


def inrange(coord):
    x, y = coord
    return 0 <= x <= maxc and 0 <= y <= maxc


# def getcoord():
#     for i, a in enumerate(inp):
#         for j in range(i + 1, len(inp)):
#             b = inp[j]
#             for coord in inters(a, b):
#                 if inrange(coord) and not any(isin(coord, bit) for bit in inp):
#                     return coord


def findhole(ytarg):
    evs = []
    for sx, sy, bx, by in inp:
        d = abs(sx - bx) + abs(sy - by)
        r = d - abs(sy - ytarg)
        if r < 0:
            continue
        evs.append((sx - r, -1))
        evs.append((sx + r + 1, +1))

    evs.sort()
    cov = 0
    for x, d in evs:
        cov -= d
        if cov == 0 and inrange((x, ytarg)):
            return (x, ytarg)
    return None


def getcoord():
    for ytarg in range(0, 1 + maxc):
        p = findhole(ytarg)
        if p is not None:
            return p
    return None


x, y = getcoord()
print(x, y)
print(x * 4000000 + y)
