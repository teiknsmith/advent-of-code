from sys import stdin

l = [(sum(map(int, g.split('\n'))))
     for g in stdin.read().strip().split('\n\n')]
print(sum(sorted(l, reverse=True)[:3]))