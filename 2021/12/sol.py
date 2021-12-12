from sys import stdin
from collections import defaultdict, deque

def solve():
    es = defaultdict(lambda: set())
    for l in lines():
        u, v = l.split('-')
        es[u].add(v)
        es[v].add(u)
    paths = {k:set() for k in es}
    tovis = deque()
    tovis.append(('start', "", False))
    while tovis:
        u, p, hasdup = tovis.popleft()
        for v in es[u]:
            doprint = False
            if doprint:
                print(f"{p} going to {v}, {hasdup=}")
            if ((not hasdup) or (v.isupper() or v not in p)) and (v != "start"):
                if doprint:
                    print("   actually")
                newpath = p + f",{v}"
                if v != 'end':
                    tovis.append((v, newpath, hasdup or (v.islower() and (v in p))))
                paths[v].add(newpath)
    print(len(paths['end']))
    pass


def lines():
    return stdin.read().strip().split('\n')

if __name__ == '__main__':
    solve()
