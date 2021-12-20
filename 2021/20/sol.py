import numpy as np
from sys import stdin
import functools as fntls
import operator as op


def step(g, alg, stepnum):
    h = len(g)
    w = len(g[0])

    res = g.copy()

    for i in range(1, h - 1):
        for j in range(1, w - 1):
            lookup = int(''.join(
                map(str, map(int, g[i - 1:i + 2, j - 1:j + 2].flatten()))),
                         base=2)
            res[i, j] = alg[lookup]

    res = res[1:-1, 1:-1]
    res = np.pad(res, 2, constant_values=stepnum % 2 == 0)

    return res


def solve():
    gs = groups()
    algo = list(map(fntls.partial(op.eq, '#'), gs[0][0]))

    g = np.array([list(map(fntls.partial(op.eq, '#'), l)) for l in gs[1]])
    g = np.pad(g, 2)

    for i in range(50):
        g = step(g, algo, i)

    print(sum(g.flatten()))


def groups():
    return [g.split('\n') for g in stdin.read().strip().split('\n\n')]


if __name__ == '__main__':
    solve()
