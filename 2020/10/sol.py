import sys
from collections import deque as deq
import functools

lines = sorted([int(l) for l in sys.stdin.readlines()] + [0])
lines.append(lines[-1] + 3)
diff = []
for i in range(1, len(lines)):
    diff.append(lines[i] - lines[i-1])
print(lines)
print(diff)

def count(l, el):
    c = 0
    for b in l:
        if b == el:
            c += 1
    return c

c1 = count(diff, 1)
c3 = count(diff, 3)
resa = c1 * c3

seq1cs = [0] * len(diff)

num1s = 0
for el in diff:
    if el == 1:
        num1s += 1
    else:
        seq1cs[num1s] += 1
        num1s = 0
print(seq1cs)

@functools.lru_cache(maxsize=None)
def num1arrs(seqlen):
    if seqlen <= 0:
        return 0
    elif seqlen == 1:
        return 1
    elif seqlen == 2:
        return 2
    elif seqlen == 3:
        return 4
    else:
        return num1arrs(seqlen - 1) + num1arrs(seqlen - 2) + num1arrs(seqlen - 3)

arrs = 1
for seqlen, nseqs in enumerate(seq1cs):
    if nseqs and seqlen:
        print(nseqs, seqlen, "s --> ", num1arrs(seqlen), " ** ", nseqs)
        arrs *= (num1arrs(seqlen) ** nseqs)

print(arrs)
