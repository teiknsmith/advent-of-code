import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
e = enumerate

pub_keys = [int(l) for l in sys.stdin.readlines()]
mod = 20201227

loop = 1
loops = [None, None]
while not any(loops):
    poss_key = pow(7, loop, mod)
    if poss_key == pub_keys[0]:
        loops[0] = loop
    if poss_key == pub_keys[1]:
        loops[1] = loop
    loop += 1

if loops[1]:
    sola = pow(pub_keys[0], loops[1], mod)
else:
    sola = pow(pub_keys[1], loops[0], mod)

solb = None
    
print("Part 1: ", sola)

print("Part 2: ", solb)

