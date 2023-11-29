from sys import stdin

cmds = [None if l.startswith('noop') else int(l.split()[1]) for l in stdin]
# {*map(print, cmds)}
r = 0
t = 0
x = 1
xl = [1]
for cmd in cmds:
    px = x
    pt = t
    if cmd is None:
        xl.append(x)
    else:
        xl.append(x)
        xl.append(x)
        x += cmd

for i in range(20, 221, 40):
    # print(i, xl[i])
    r += i * xl[i]
print(r)

crt = [[' '] * 40 for _ in range(6)]
for ij, x in enumerate(xl, -1):
    i, j = divmod(ij, 40)
    if abs(j - x) <= 1:
        crt[i][j] = '#'

print('\n'.join(''.join(r) for r in crt))