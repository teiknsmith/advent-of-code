import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
import string

e = enumerate


def weval(line, indent=0):
    res = 0
    digits = []
    op = None
    inparens = 0
    for i, c in e(line):
        if inparens:
            if c == '(':
                inparens += 1
            elif c == ')':
                inparens -= 1
            continue
#        print(f"{' ' * indent}looking at {c}, res:{res}, digits:{digits}, op:{op}")
        rhs = None
        if c == '(':
            rhs = weval(line[i+1:], indent+3)
            if op:
                if op == '*':
                    res *= rhs
                elif op == '+':
                    res += rhs
            else:
                res = rhs
            inparens = 1
        elif c == ')':
            if digits:
                rhs = int(''.join(digits))
                digits = []
                if op:
                    if op == '*':
                        res *= rhs
                    elif op == '+':
                        res += rhs
                else:
                    res = rhs
            return res
        elif c in "*+":
            op = c
        elif c in string.digits:
            digits.append(c)
        elif c in string.whitespace:
            if digits:
                rhs = int(''.join(digits))
                digits = []
                if op:
                    if op == '*':
                        res *= rhs
                    elif op == '+':
                        res += rhs
                else:
                    res = rhs
        else:
            print("WHAT!!")
    return res

lines = [weval(l) for l in sys.stdin.readlines()]


sola = sum(lines)



solb = None


print("Part 1: ", sola)

print("Part 2: ", solb)

