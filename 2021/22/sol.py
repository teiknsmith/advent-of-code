from sys import stdin
import functools as fntls
import operator as op
import re

INF = float('inf')


def overlaps1d(c1, c2):
    return not (c1[1] < c2[0] or c2[1] < c1[0])


def pairs(c):
    return (c[i:i + 2] for i in range(0, len(c), 2))


def overlaps(c1, c2):
    return all(map(overlaps1d, pairs(c1), pairs(c2)))


def spans(og, rm):
    """Return list of keep spans and rm spans"""
    ogl, ogr = og
    rml, rmr = rm
    if not overlaps1d(og, rm):
        #         __og__
        # _rm__
        return [og], []
    if rml <= ogl <= ogr <= rmr:
        #      __og__
        # ______rm_____
        return [], [og]
    elif rml <= ogl <= rmr < ogr:
        #    ___og___
        #  ___rm___
        return [(rmr + 1, ogr)], [(ogl, rmr)]
    elif ogl < rml <= ogr <= rmr:
        #  ___og___
        #    ___rm___
        return [(ogl, rml - 1)], [(rml, ogr)]
    elif ogl < rml <= rmr < ogr:
        #  ___og________
        #    ___rm___
        return [(ogl, rml - 1), (rmr + 1, ogr)], [rm]
    else:
        raise NotImplementedError(f"Unknown overlap type: {og=}, {rm=}")


def join(span_pairs, og, accum, i=0, moddy=None):
    if moddy is None:
        moddy = list(og)
    if i >= len(span_pairs):
        return

    keep, remove = span_pairs[i]
    for kl, kr in keep:
        moddy[i * 2] = kl
        moddy[i * 2 + 1] = kr
        accum.add(tuple(moddy))
    for rl, rr in remove:
        moddy[i * 2] = rl
        moddy[i * 2 + 1] = rr
        join(span_pairs, og, accum, i + 1, moddy)


def remainder_cubes(og, rm):
    span_pairs = list(map(spans, pairs(og), pairs(rm)))
    res = set()
    join(span_pairs, og, res)
    return res


def vol(c):
    return fntls.reduce(
        op.mul, map(op.sub, map(fntls.partial(op.add, 1), c[1::2]), c[::2]))


# PART 1
N = 50

# PART 2
# N = INF


def solve():
    cubes = set()
    lpatt = re.compile(
        r"(on|off) x=(-?\d*)..(-?\d*),y=(-?\d*)..(-?\d*),z=(-?\d*)..(-?\d*)")
    for l in lines():
        match = lpatt.match(l)
        new_is_on = match.group(1) == 'on'
        new_cube = tuple(map(int, match.group(*list(range(2, 8)))))
        if not all(abs(el) <= N for el in new_cube):
            continue
        rm = set()
        mk = set()
        for cube in cubes:
            if overlaps(cube, new_cube):
                mk |= remainder_cubes(cube, new_cube)
                rm.add(cube)
        cubes -= rm
        cubes |= mk
        if new_is_on:
            cubes.add(new_cube)

    print(sum(map(vol, cubes)))


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
