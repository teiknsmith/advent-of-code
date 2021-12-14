from sys import stdin


def solve():
    g = [[0] * 1000 for _ in range(1000)]
    for l in lines():
        if l.startswith("turn"):
            bits = l.split()
            newval = 1 if bits[1] == 'on' else -1
            i1, j1 = map(int, bits[2].split(','))
            i2, j2 = map(int, bits[4].split(','))
            for i in range(i1, i2 + 1):
                for j in range(j1, j2 + 1):
                    g[i][j] += newval
                    g[i][j] = max(g[i][j], 0)
        else:
            bits = l.split()
            i1, j1 = map(int, bits[1].split(','))
            i2, j2 = map(int, bits[3].split(','))
            for i in range(i1, i2 + 1):
                for j in range(j1, j2 + 1):
                    g[i][j] += 2  #not g[i][j]
    count = 0
    for r in g:
        for v in r:
            if v:
                count += v
    print(count)


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
