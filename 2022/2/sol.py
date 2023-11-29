from sys import stdin


def score(s):
    print(s, end='->')
    a, b = s.split()
    me = "XYZ".find(b)
    other = "ABC".find(a)
    x = ((me + other) + 5) % 3 + 1
    res = 3 * me
    print(other, me, x, res)
    return res + x


print(sum(map(score, stdin.read().strip().split('\n'))))