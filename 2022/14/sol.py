from sys import stdin

lines = list(
    list(tuple(map(int, b.split(','))) for b in l.split()[::2]) for l in stdin)
xs = [x for line in lines for x, y in line]
ys = [y for line in lines for x, y in line]
xlo, xhi = min(xs), max(xs)
ylo, yhi = min(ys), max(ys)
xlo -= 3
xhi += 3
ylo = 0
xhi = max(xhi, 500 + yhi + 20)

g = [['.'] * xhi for _ in range(yhi + 2)] + [['#'] * xhi]

for line in lines:
    px, py = line[0]
    for x, y in line[1:]:
        dx = (x - px) // abs(x - px) if x != px else 0
        dy = (y - py) // abs(y - py) if y != py else 0
        sx, sy = px, py
        while (sx, sy) != (x, y):
            g[sy][sx] = '#'
            sx += dx
            sy += dy
        g[y][x] = '#'
        px, py = x, y
g[0][500] = '+'

for k in range(int(1e6)):
    i, j = 0, 500
    while 1:
        # # Part 1
        # if i > yhi:
        #     break

        if g[i + 1][j] == '.':
            i += 1
        elif g[i + 1][j - 1] == '.':
            i += 1
            j -= 1
        elif g[i + 1][j + 1] == '.':
            i += 1
            j += 1
        else:
            g[i][j] = 'o'
            break

    # # Part 1
    # if i > yhi:
    #     break

    # Part 2
    if (i, j) == (0, 500):
        k += 1
        break
print(k)
{*map(print, (''.join(r[xlo - 4:xhi]) for r in g))}
