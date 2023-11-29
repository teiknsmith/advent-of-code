from sys import stdin

og, ds = (l.split('\n') for l in stdin.read().rstrip().split('\n\n'))
n = int(og[-1].split()[-1])
sts = [[] for _ in range(1 + n)]
for l in og[-2::-1]:
    for i, c in enumerate(l[1::4], 1):
        if c != ' ':
            sts[i].append(c)
# {*map(print, sts)}
for l in ds:
    _, r, _, f, _, t = l.split()
    r, f, t = map(int, (r, f, t))
    sts[t] += sts[f][-r:]
    sts[f] = sts[f][:-r]
    # for _ in range(r):
    #     sts[t].append(sts[f].pop())
print(''.join(st[-1] for st in sts[1:]))