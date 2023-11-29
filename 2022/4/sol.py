from sys import stdin


def f(l):
    (a, b), (c, d) = map(lambda p: map(int, p.split('-')), l.split(','))
    return not (b < c or d < a)
    return a <= c <= d <= b or c <= a <= b <= d


print(sum(1 for l in stdin if f(l)))