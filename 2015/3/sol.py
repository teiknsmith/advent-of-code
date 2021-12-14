from sys import stdin


def solve():
    cs = [[0, 0], [0, 0]]
    a = set([(0, 0)])
    i = 0
    for c in input():
        i = 1 - i
        if c == '>':
            cs[i][0] += 1
        elif c == '<':
            cs[i][0] -= 1
        elif c == '^':
            cs[i][1] += 1
        elif c == 'v':
            cs[i][1] -= 1
        a.add(tuple(cs[i]))
    print(len(a))


if __name__ == '__main__':
    solve()
