import sys
from collections import deque as deq
import functools
import math
import numpy as np
lines = [(l[0], int(l[1:])) for l in sys.stdin.readlines()]


def rot(t):
    return np.array([
        [math.cos(math.radians(t)), -math.sin(math.radians(t))],
        [math.sin(math.radians(t)), math.cos(math.radians(t))]])

angle = 0
delta = [1, 0]
pos = [0, 0]
way = [10,1]
for l in lines:
    if l[0] == 'N':
        way[1] += l[1]
    elif l[0] == 'E':
        way[0] += l[1]
    elif l[0] == 'S':
        way[1] -= l[1]
    elif l[0] == 'W':
        way[0] -= l[1]
    elif l[0] in "LR":
        angle = l[1]
        if l[0] == 'R':
            angle = -angle
        mat = rot(angle)
        #print(mat)
        way = np.matmul(mat, np.transpose(way))
    elif l[0] == 'F':
        uni = [0,0]
        uni[0] = l[1] * way[0]
        uni[1] = l[1] * way[1]
        pos[0] = pos[0] + uni[0]
        pos[1] = pos[1] + uni[1]
#    print(pos)
#    print(way)
         

print (abs(pos[0]) + abs(pos[1]))
res1 = None
