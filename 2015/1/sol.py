import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
e = enumerate

floor = 0
lines = [l for l in sys.stdin.readlines()]
i = 0
for c in lines[0]:
    floor += 1 if c == '(' else -1
    if floor == -1:
        solb = i
        break
    i += 1
    

sola = floor





print("Part 1: ", sola)

print("Part 2: ", solb)

