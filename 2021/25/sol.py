from sys import stdin


def solve():
    cucs = {k: set() for k in ">v."}
    for i, r in enumerate(lines()):
        for j, v in enumerate(r):
            cucs[v].add((i, j))
    del cucs['.']
    h, w = i + 1, j + 1
    trs = {
        '>': lambda t: (t[0], (t[1] + 1) % w),
        'v': lambda t: ((t[0] + 1) % h, t[1]),
    }
    changed = True
    nsteps = 0
    while changed:
        nsteps += 1
        changed = False
        for cucfam in ">v":
            mkcucs = set()
            rmcucs = set()
            tr = trs[cucfam]
            for cuc in cucs[cucfam]:
                newcuc = tr(cuc)
                if not any((newcuc in fam) for fam in cucs.values()):
                    mkcucs.add(newcuc)
                    rmcucs.add(cuc)
            if rmcucs:
                changed = True
            cucs[cucfam] -= rmcucs
            cucs[cucfam] |= mkcucs

    print(nsteps)


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
