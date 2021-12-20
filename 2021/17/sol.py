import math
import re
from collections import defaultdict

INF = float('inf')


def vx_for_targ(t, x, is_moving=None):
    if 2 * x >= (t**2 + t) if is_moving is None else is_moving:
        return x / t + (t - 1) / 2
    else:
        return (math.sqrt(1 + 8 * x) - 1) / 2


def rect_area(x1, x2, y1, y2):
    if x2 < x1 or y2 < y1:
        return 0
    return (x2 - x1 + 1) * (y2 - y1 + 1)


def calc(x1, x2, y1, y2):
    # for completeness's sake, I copied part 1 from the old calc here
    print(((-y1 - 1) * -y1) / 2)

    vx_for_left = math.ceil(vx_for_targ(None, x1, False))
    vx_for_right = math.floor(vx_for_targ(None, x2, False))
    vxs = defaultdict(lambda: (vx_for_left, vx_for_right))
    for t in range(1, vx_for_left):
        vxs[t] = (math.ceil(vx_for_targ(t, x1)),\
                  math.floor(vx_for_targ(t, x2)))
    for t in range(vx_for_left, vx_for_right + 1):
        vxs[t] = (vx_for_left, math.floor(vx_for_targ(t, x2)))

    # y is flipped bc it made more sense in my head
    ymin = -y2
    ymax = -y1
    triangle_num = 0
    prev_rect = [INF, INF, -INF, -INF]
    tot = 0
    for t in range(-2 * y1 + 1):
        t += 1
        triangle_num += t
        min_vy = math.ceil((ymin - triangle_num) / t) + 1
        max_vy = math.floor((ymax - triangle_num) / t) + 1
        if max_vy < min_vy:
            continue

        # flipping y back for these. don't @ me
        rect = [*vxs[t], -max_vy, -min_vy]
        overlap = [prev_rect[0], rect[1], rect[2], prev_rect[3]]
        tot += rect_area(*rect) - rect_area(*overlap)

        prev_rect = rect
    print(tot)


def lands(vx, vy, x1, x2, y1, y2):
    x, y = 0, 0
    t = 0
    ts = []
    while y >= 2 * y1 - 10 and x <= 2 * x2 + 10:
        if btwne(x, x1, x2) and btwne(y, y1, y2):
            ts.append(t)
        x += vx
        y += vy
        vy -= 1
        vx = max(vx - 1, 0)
        t += 1
    return ts


def oldcalc(x1, x2, y1, y2):
    # for completeness's sake, I copied part 1 from the old calc here
    print(((-y1 - 1) * -y1) / 2)

    rs = defaultdict(lambda: [INF, -INF, INF, -INF])

    c = 0
    for vx in range(1, x2 + 1):
        for vy in range(y1, -y1):
            ts = lands(vx, vy, x1, x2, y1, y2)
            if ts:
                c += 1
                for t in ts:
                    rs[t][0] = min(rs[t][0], vx)
                    rs[t][1] = max(rs[t][1], vx)
                    rs[t][2] = min(rs[t][2], vy)
                    rs[t][3] = max(rs[t][3], vy)
    for t in sorted(rs):
        print(t, rs[t])
    print(c)


"""
# I'm keeping this here as a lesson to myself, and a possible future project.
# I didn't need to optimize the search with math, but I thought I would 'be smart'.
# then after an hour or two and still not getting there, I did the `calc` above.
# This is the state these functions were in when I switched.
def vxfortarg(t, x):
    iflte = (math.sqrt(1 + 8 * x) - 1) / 2
    ifgt = x / t - (1 - t) / 2
    if iflte <= t and ifgt > t:
        print(f'how???? {(t,x,iflte,ifgt)=}')
    return iflte


def howmanyvsx(t, x1, x2):
    return 1 + math.floor(vxfortarg(t, x2)) - math.ceil(vxfortarg(t, x1))

def oldcalc(x1, x2, y1, y2):
    # print(x1, x2, y1, y2)

    nsteps_high = -2 * y1
    max_height = ((-y1 - 1) * -y1) / 2
    vy_for_that = -y1 - 1
    vx_for_left_edge = vxfortarg(nsteps_high, x1)
    vx_for_right_edge = vxfortarg(nsteps_high, x2)

    # for hit_height in range(-y2, -y1):
    #     nsteps = 2*hit_height
    #     print(nsteps,': ', vxfortarg(nsteps, x1), vxfortarg(nsteps, x2))

    uppers = (y2 - y1) * (1 + math.floor(vxfortarg(nsteps_high, x2)) -
                          math.ceil(vxfortarg(nsteps_high, x1)))

    wacks = 0
    for possvy in range(0, y2, -1):
        y = 0
        for t in range(10000):
            y += possvy
            possvy -= 1
            if btwne(y, y2, y1):
                wacks += howmanyvsx(t, x1, x2)
            elif y < y1:
                break

    straight_ins = (x2 - x1 + 1) * (y2 - y1 + 1)

    print(uppers)
    print(wacks)
    print(straight_ins)
"""


def solve():
    x1, x2, y1, y2 = map(
        int,
        re.match(r"target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)",
                 input()).groups())
    # just in case they aren't actually in order
    x1, x2 = sorted((x1, x2))
    y1, y2 = sorted((y1, y2))
    calc(x1, x2, y1, y2)


def btwne(v, l, h):
    return (v >= l and v <= h) or (v <= l and v >= h)


if __name__ == '__main__':
    solve()
