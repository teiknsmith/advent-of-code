from sys import stdin


def f(l):
    a, b, c = map(set, l)
    print(a)
    print(b)
    print(c)
    c = (a & b & c).pop()
    r = ord(c) + ((1 - ord('a')) if 'a' <= c <= 'z' else (27 - ord('A')))
    print(c, 'a' <= c, c <= 'z', r, l)
    return r


ls = list(stdin.read().strip().split('\n'))
print(sum(map(f, (ls[i:i + 3] for i in range(0, len(ls), 3)))))
