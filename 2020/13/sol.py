import sys
from collections import deque as deq
import functools
import math
import numpy as np
e = enumerate

#lines = [(l[0], int(l[1:])) for l in sys.stdin.readlines()]
lines = sys.stdin.readlines()

mtime = int(lines[0])
busses = [int(el) for el in lines[1].split(',') if el != 'x']

res = sorted([(el - mtime % el, el) for el in busses])[0]
sola = res[0] * res[1]

print(sola)
busses = sorted([(int(el), (int(el) - i) % int(el)) for i, el in e(lines[1].split(',')) if el != 'x'], reverse=True)

print(busses)
print('hi')
guess = busses[0][1]
to_add = busses[0][0]
for bus in busses[1:]:
    while guess%bus[0] != bus[1]:
        guess += to_add
    to_add *= bus[0]
    print(guess, to_add)

print(guess)
