from sys import stdin


def solve():
    s = 0
    r = 0
    for l in lines():
        l, w, h = map(int, l.split('x'))
        ars = [l * w, w * h, h * l]
        s += (2 * sum(ars) + min(ars))
        r += (sum([l, w, h]) - max([l, w, h])) * 2 + l * w * h
    print(s)
    print(r)
    pass


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
