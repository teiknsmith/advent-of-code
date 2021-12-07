import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
e = enumerate


rlines, tlines = [g.strip().split('\n') for g in sys.stdin.read().split('\n\n')]

rules = dict()
def rulefunc(idstr, patstr):
    options = [pat.split() for pat in patstr.split('|')]
    def patfun(possible_to_match, indent=0):
        #print(f'{"|   "*indent}check {possible_to_match} against {idstr}: {patstr}')
        possible_remains = set()
        for opt in options:
            remainings = set(possible_to_match)
            for piece in opt:
                remainings = ({remain[1:] for remain in remainings if (remain and remain[0] == piece[1])}
                                      if piece[0] == '"' else rules[int(piece)](remainings, indent+1))
                if not remainings:
                    break
            if remainings:
                possible_remains = possible_remains.union(remainings)
        #print(f'{"|   "*indent}done: {possible_remains}')
        return possible_remains
    return patfun
for r in rlines:
    idstr, patstr = r.split(': ')
    if idstr == '8':
        patstr = "42 | 42 8"
    elif idstr == '11':
        patstr = "42 31 | 42 11 31"
    patfun = rulefunc(idstr, patstr)
    rules[int(idstr)] = patfun

def matches(to_match):
    possible_remains = rules[0]({to_match})
    return any(map(lambda p: not p, possible_remains))

goods = [t for t in tlines if matches(t)]
sol = len(goods)

print(sol)

