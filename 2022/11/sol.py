from sys import stdin
from collections import deque
from math import gcd

ms = []

LCM = 1


def lcm(a, b):
    return a * b // gcd(a, b)


class Monkey:

    def __init__(self, txt):
        global LCM
        _, its, op, test, ift, iff = txt.split('\n')
        self.txt = txt
        self.its = deque(map(int, its.split(' ', 4)[-1].split(', ')))
        eq = ' '.join(op.split()[-3:])

        # print(eq)

        def upd(old):
            new = eval(eq)
            # new //= 3
            new %= LCM
            return new

        self.upd = upd

        test = int(test.split()[-1])
        LCM = lcm(LCM, test)
        self.test = lambda x: x % test == 0
        self.ift = int(ift.split()[-1])
        self.iff = int(iff.split()[-1])

        self.ctr = 0

    def makemove(self):
        # print(self.its)
        self.ctr += len(self.its)
        for v in self.its:
            v = self.upd(v)
            ms[self.ift if self.test(v) else self.iff].its.append(v)
        self.its = deque()

    def __repr__(self):
        return str(self.its)


ms += list(map(Monkey, stdin.read().strip().split('\n\n')))

for i in range(1, 10001):
    for m in ms:
        m.makemove()
    if i in {1, 20} or i % 1000 == 0:
        print('Round', i)
        for mi, m in enumerate(ms):
            print(mi, m.ctr)
        print()
cs = [m.ctr for m in ms]
cs.sort()
print(cs[-2] * cs[-1])
