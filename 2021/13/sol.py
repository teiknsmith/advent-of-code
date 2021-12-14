from sys import stdin
import functools as fntls

e = enumerate
INF = float('inf')


def one_d_fold(f):
    return lambda c: c if c < f else 2 * f - c


def hfold(h):
    return lambda x, y: (x, one_d_fold(h)(y))


def vfold(v):
    return lambda x, y: (one_d_fold(v)(x), y)


def fold(orientation, v):
    return hfold(v) if orientation == 'y' else vfold(v)


def solve():
    ogpts = []
    folds = []
    for l in lines():
        if not l:
            continue
        if l[0] == 'f':
            let, v = l.split()[2].split('=')
            v = int(v)
            folds.append(fold(let, v))
        else:
            ogpts.append(tuple(map(int, l.split(','))))

    pt1pts = set()
    respts = set()
    for coord in ogpts:
        respts.add(fntls.reduce(lambda c, f: f(*c), folds, coord))
        pt1pts.add(folds[0](*coord))

    h = max(y for _, y in respts) + 1
    w = max(x for x, _ in respts) + 1
    g = [[' '] * w for _ in range(h)]
    for x, y in sorted(respts):
        g[y][x] = '#'

    for r in g:
        print(''.join(r))

    print(len(pt1pts))


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
