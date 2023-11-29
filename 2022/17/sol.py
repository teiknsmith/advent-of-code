from itertools import *

W = 7
gas = input()
gasgen = cycle(gas)


def getgas():
    c = next(gasgen)
    return (c == '>') - (c == '<')


def tocoords(raw):
    rows = reversed(raw.split('\n'))
    res = set()
    for i, row in enumerate(rows):
        for j, v in enumerate(row):
            if v == '#':
                res.add((i, j))

    return res


pieces = list(
    map(tocoords, [
        "####",
        ".#.\n###\n.#.",
        "..#\n..#\n###",
        "#\n#\n#\n#",
        "##\n##",
    ]))
piecegen = cycle(pieces)


def getpiece():
    return set(next(piecegen))


g = []
h = 0

doprint = False


def place(g, i, j, c='#'):
    while not (i < len(g)):
        g.append(['.'] * W)
    g[i][j] = c


def draw(g, piece=None):
    if piece is not None:
        g = list(list(r) for r in g)
        for i, j in piece:
            place(g, i, j, '@')
    for r in list(reversed(g))[:20]:
        print(''.join(r))
    print()


def tr(s, di, dj):
    global doprint
    if doprint:
        print(f'tr by {di},{dj}')
    nxt = {(i + di, j + dj) for i, j in s}
    ret = nxt, True
    for i, j in nxt:
        if not (0 <= j < W and 0 <= i and
                ((not i < len(g)) or g[i][j] == '.')):
            ret = s, False
            break
    if doprint:
        draw(g, ret[0])
    return ret


for k in range(695):
    piece = getpiece()
    piece, _ = tr(piece, h + 3, 2)
    doprint = k == 692
    if doprint:
        draw(g, piece)
    piece, _ = tr(piece, 0, getgas())
    piece, moved = tr(piece, -1, 0)
    while moved:
        piece, _ = tr(piece, 0, getgas())
        piece, moved = tr(piece, -1, 0)
    for i, j in piece:
        h = max(h, i + 1)
        # place(g, i, j, '#')
        place(g, i, j, chr(ord('A') + k % 26))

# draw(g)
print(h)