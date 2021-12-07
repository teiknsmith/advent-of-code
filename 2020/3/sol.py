import sys

l = sys.stdin.read().split('\n')
del l[-1]
w = len(l[0])
steps = [
    (1, 1),
    (3, 1),
    (5, 1),
    (7, 1),
    (1, 2)
]
c = 1
for step in steps:
    j = 0;
    count = 0;
    for el in l[::step[1]]:
        if el[j] == '#':
            count += 1
        j += step[0]
        j %= w
    c *= count

print(c)
