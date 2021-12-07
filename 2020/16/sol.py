import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re

e = enumerate
lines = [l.strip() for l in sys.stdin.readlines()]

rules = []
mine = ""
nearby = []

addto = "rules"
for l in lines:
    if l:
        if l == "your ticket:":
            addto = "mine"
        elif l == "nearby tickets:":
            addto = "nearby"
        elif addto == "rules":
            rules.append(l)
        elif addto == "mine":
            mine = l
        elif addto == "nearby":
            nearby.append(l)

def tester(rule):
    a, b, c, d = [int(el) for el in re.match(r'.*: (\d*)-(\d*) or (\d*)-(\d*)', rule).groups()]
    return lambda n: (n >= a and n <= b) or (n >= c and n <= d)

tests = [tester(el) for el in rules]

nearby = [[int(el) for el in l.split(',')] for l in nearby]

num_bad = 0
for n in nearby:
    for num in n:
        if not any(map(lambda f:f(num), tests)):
            num_bad += num

sola = num_bad


valid_near = np.array([n for n in nearby if all(any(map(lambda f:f(el), tests)) for el in n)])
fields = {rule.split(':')[0]:tester(rule) for rule in rules}
mine = [int(el) for el in mine.split(',')]

possibles = [{f for f, t in fields.items() if all(map(t, valid_near[:,i]))} for i,_ in e(mine)]

while not all(len(p) == 1 for p in possibles):
    fixed = {el for p in possibles if len(p) == 1 for el in p}
    possibles = [p if len(p) == 1 else (p - fixed) for p in possibles]

solb = 1
for i, nameset in e(possibles):
    if list(nameset)[0].startswith('departure'):
        print("found one!")
        solb *= mine[i]


print("Part 1: ", sola)

print("Part 2: ", solb)

