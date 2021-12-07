import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
e = enumerate


cups = list(map(int, list(sys.stdin.read().strip())))
mincup = min(cups)
maxcup = max(cups)
cups = (0, cups)
np.core.arrayprint._line_width = 220

class Mover:
    def __init__(self):
        self.deltas = []
    def move(self, cups):
        active, lst = cups
        """
        print(active)
        print('cups:', end='')
        for i, el in e(lst):
            if i == active:
                print(f' ({el})', end='')
            else:
                print(f' {el}', end='')
        print()
        self.deltas.append(np.diff(lst))
        #print(self.deltas[-1])
        if len(self.deltas) >= 2:
            print(self.deltas[-1] - self.deltas[-2])        
        """
        grab = lst[active + 1:active+4]
        frontgrab = max(0, 3 - len(grab))
        #print(frontgrab)
        if frontgrab:
            grab += lst[:frontgrab]
            
        #print(f'gra: {grab}')
        destcup = lst[(active ) % len(lst)] - 1
            
        for _ in range(3-frontgrab):
            del lst[(active + 1) % len(lst)]
        for _ in range(frontgrab):
            del lst[0]
        
        while destcup in grab or destcup < mincup:
            destcup -= 1
            if destcup < mincup:
                destcup = maxcup
        #print(f'dest {destcup}')
        #print()

        for i, el in e(lst):
            if el == destcup:
                break

        for el in grab[::-1]:
            lst.insert(i + 1, el)
        return ((active - frontgrab + (4 if i < (active ) else 1)) % len(lst), lst)

    def make_moves(self, n, cups):
        for _ in range(n):
            cups = self.move(cups)
        return cups

cups = Mover().make_moves(100, cups)
lst = cups[1]
foundone = False
i = 0
res = []
while True:
    if lst[i] == 1 and foundone:
        break
    if foundone:
        res.append(lst[i])
    if lst[i] == 1:
        foundone = True
    i += 1
    i %= len(lst)
        
        
print(''.join(map(str, res)))
