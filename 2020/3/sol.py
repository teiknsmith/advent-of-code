import sys

lines = sys.stdin.read().split('\n')
del lines[-1]
w = len(lines[0])
steps = [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]
res = 1
for step in steps:
    j = 0
    count = 0
    for row in lines[::step[1]]:
        if row[j] == '#':
            count += 1
        j += step[0]
        j %= w
    res *= count

print(res)
