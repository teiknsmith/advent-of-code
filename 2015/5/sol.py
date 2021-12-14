from collections import Counter
from sys import stdin


def nice(l):
    counts = Counter(l)
    if sum(counts[k] for k in "aeiou") < 3:
        return False
    if any(bad in l for bad in "ab cd pq xy".split()):
        return False
    prev_c = l[0]
    for c in l[1:]:
        if c == prev_c:
            return True
        prev_c = c
    return False


def nice2(l):
    pairs = set()
    prev_c = l[0]
    hasrep = False
    hasgap = False
    for c, next_c in zip(l[1:], l[2:]):
        if (c, next_c) in pairs:
            if hasgap:
                return True
            hasrep = True
        if prev_c == next_c:
            if hasrep:
                return True
            hasgap = True
        pairs.add((prev_c, c))
        prev_c = c

    return False


def solve():
    print(len(list(l for l in lines() if nice2(l))))


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
