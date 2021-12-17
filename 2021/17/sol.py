import math
import re



def lands(vx, vy, x1, x2, y1, y2):
    x, y = 0, 0
    while y >= 2 * y1 - 10:
        if btwne(x, x1, x2) and btwne(y, y1, y2):
            return True
        x += vx
        y += vy
        vy -= 1
        vx = max(vx - 1, 0)
    return False


def calc(x1, x2, y1, y2):
    # for completeness's sake, I copied part 1 from the old calc here
    print(((-y1 - 1) * -y1) / 2)

    c = 0
    for vx in range(1, x2 + 1):
        for vy in range(y1, -y1):
            if lands(vx, vy, x1, x2, y1, y2):
                c += 1
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
