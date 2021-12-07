import sys
from collections import deque as deq
import functools
import math
import numpy as np

lines = [int(l) for l in sys.stdin.readlines()[0].split(',')]

used = dict()
last=0
turn = 0
for line in lines:
    used[line] = [turn]
    turn += 1
    last = line
print(used, last)
while True:
    if len(used[last]) == 1:
        last = 0
        used[last].append(turn)
    else:
        last = used[last][-1] - used[last][-2]
        if last in used:
            used[last].append(turn)
        else:
            used[last] = [turn]
#    print(f'{turn}, {used}')
    turn += 1
    if turn == 30000000:
        sola = last
        break



solb = None


print("Part 1: ", sola)

print("Part 2: ", solb)

