import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
import string

e = enumerate

def tokenize(l):
    res = []
    prev_c = None
    for c in l:
        if c in '()*+':
            res.append(c)
        elif c in string.digits:
            if prev_c and prev_c in string.digits:
                res[-1].append(c)
            else:
                res.append(c)
        prev_c = c
    return res
OPS = "*+"
def shunt(tokens):
    op_stack = []
    rpn = []
    for token in tokens:
        if token == ')':
            while op_stack[-1] != '(':
                rpn.append(op_stack.pop())
            op_stack.pop()
        elif token == '(':
            op_stack.append('(')
        elif token in "+*":
            while op_stack and op_stack[-1] in OPS and OPS.find(op_stack[-1]) >= OPS.find(token):
                rpn.append(op_stack.pop())
            op_stack.append(token)
        else:
            rpn.append(token)
    while op_stack:
        rpn.append(op_stack.pop())
    return rpn

def rpneval(tokens):
    stack = []
    for t in tokens:
        if t in OPS:
            lhs, rhs = stack.pop(), stack.pop()
            stack.append(str(eval(lhs + t + rhs)))
        else:
            stack.append(t)
    return int(stack[-1])

def weval(l):
    tokens = tokenize(l)
    rpn = shunt(tokens)
    return rpneval(rpn)

lines = [weval(l) for l in sys.stdin.readlines()]

solb = sum(lines)

print("Part 2: ", solb)

