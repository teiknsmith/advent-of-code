from functools import *
from sys import stdin
import re
from collections import defaultdict as dd

T = 30

vs = list()
flowvs = list()
g = dict()
fl = dict()

for l in stdin.read().strip().split('\n'):
    # print(l)
    v, f, t = re.match(
        r'Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)',
        l).groups()
    f = int(f)
    t = list(t.split(', '))
    # print(v, f, t, sep='|')
    g[v] = t
    fl[v] = f
    vs.append(v)
    if f:
        flowvs.append(v)

doprint = len(vs) < 15
doprint = False
vs.sort()
d = dd(lambda: dd(lambda: float('inf')))
dir = dd(lambda: dd(lambda: None))

for u in vs:
    # print(u)
    for v in g[u]:
        d[u][v] = 1
        dir[u][v] = v
        # print('   ', v)
# {*map(print, sorted((v, fl[v]) for v in flowvs))}
for k in vs:
    for u in vs:
        for v in vs:
            new = d[u][k] + d[k][v]
            if new < d[u][v]:
                d[u][v] = new
                dir[u][v] = dir[u][k]

flowvs.sort()
flowvs = ['AA'] + flowvs
flowset = set(flowvs)
flows = [fl[v] for v in flowvs]
n = len(flowvs)
ids = {v: i for i, v in enumerate(flowvs)}
g = [dict() for _ in range(n)]
for ui, uv in enumerate(flowvs):
    for vi, vv in enumerate(flowvs[ui + 1:], ui + 1):
        # print(ui, vi)
        sc = dir[uv][vv]
        for i in range(1, 2 * len(vs)):
            if sc == vv:
                g[ui][vi] = i
                g[vi][ui] = i
                break
            if sc in flowset:
                break
            sc = dir[sc][vv]

# {*map(print, enumerate(flowvs))}
# for u, vws in enumerate(g):
#     print(u, ':')
#     for v, w in vws.items():
#         print('   ', v, w)
# print(flows)
# if doprint:
# {*map(print, dg)}

recdep = 0


@cache
def f(u, t, onvs, onfl):
    if t >= T:
        assert T - t <= 0
        return (T - t) * onfl  # sub from whoever called
        # return (
        #     (T - t) * onfl, [f"jk, didn't make it"])  # sub from whoever called
    global recdep
    tab = '  |' * recdep + '-'
    if doprint:
        print(tab, u, t, onvs, onfl)
    recdep += 1
    score = (T - t) * onfl
    opts = [score]
    # opts = [(score, [f'{t:>2}:{f"wait":>14} {score:>5}'])]
    if u not in onvs and flows[u]:
        convs = set(onvs)
        convs.add(u)
        score = f(u, t + 1, frozenset(convs), onfl + flows[u])
        # score, path = f(u, t + 1, frozenset(convs), onfl + flows[u])
        score += onfl
        opts.append(score)
        # opts.append(
        #     (score, path + [f'{t:>2}:{f"turn on {u}":>14} {score:>5}']))
    for v, w in g[u].items():
        xtrascore = f(v, t + w, onvs, onfl)
        # xtrascore, path = f(v, t + w, onvs, onfl)
        score = onfl * w + xtrascore
        opts.append(score)
        # opts.append(
        #     (score, path + [f'{t:>2}:{f"move to {v}":>14} {score:>5}']))
    r = max(opts)
    # r = max(opts, key=lambda t: t[0])
    if doprint:
        print(tab, '-->', u, t, onvs, onfl, '-->', r)
    recdep -= 1
    return r


score = f(0, 0, frozenset(), 0)
path = ['??']
# score, path = f(0, 0, frozenset(), 0)
print(score)
for el in reversed(path):
    print(el)
