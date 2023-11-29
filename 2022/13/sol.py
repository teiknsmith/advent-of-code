from sys import stdin
from functools import cmp_to_key


def cmp(a, b):
    ai = isinstance(a, int)
    bi = isinstance(b, int)
    # print(a, b, end=':')
    if ai and bi:
        # print('int int')
        if a == b:
            return 0
        return -1 if a < b else 1
    else:
        if ai:
            a = [a]
        if bi:
            b = [b]
        # print(a, b)
        for ael, bel in zip(a, b):
            r = cmp(ael, bel)
            if r:
                return r
        a, b = map(len, (a, b))
        return cmp(a, b)


dividers = [[[2]], [[6]]]
allsigs = list(dividers)
t = 0
for i, g in enumerate(stdin.read().strip().split('\n\n'), 1):
    a, b = map(eval, g.split('\n'))
    allsigs += [a, b]
    if cmp(a, b) < 0:
        t += i

print(t)
allsigs.sort(key=cmp_to_key(cmp))
divis = []
for i, sig in enumerate(allsigs, 1):
    if sig in dividers:
        divis.append(i)
print(divis[0] * divis[1])
