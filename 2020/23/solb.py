import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
e = enumerate

class CupCircle:
    class Cup:
        def __init__(self, cupid, succ):
            self.id = cupid
            self.succ = succ
        def __str__(self):
            return str(self.id)
        def circ_string(self, head=None):
            if head == self:
                return '(loop)'
            if head is None:
                head = self
            return str(self.id) + (self.succ.circ_string(head) if self.succ else '')
            
    def __init__(self, lst):
        self.lookups = dict()
        self.mincup = min(lst)
        self.maxcup = max(lst)
        tail = CupCircle.Cup(lst[-1], None)
        succ = tail
        self.lookups[lst[-1]] = tail
        for el in lst[-2::-1]:
            succ = CupCircle.Cup(el, succ)
            self.lookups[el] = succ
        tail.succ = succ
        self.head = succ

    def __str__(self):
        return self.head.circ_string()

    def move(self):
        grabhead = self.head.succ
        grabtail = grabhead
        grabs = {grabtail.id}
        for _ in range(2):
            grabtail = grabtail.succ
            grabs.add(grabtail.id)
        self.head.succ = grabtail.succ
        destid = self.head.id - 1
        while destid in grabs or destid < self.mincup:
            destid -= 1
            if destid < self.mincup:
                destid = self.maxcup
        destcup = self.lookups[destid]
        grabtail.succ = destcup.succ
        destcup.succ = grabhead
        self.head = self.head.succ

    def past_one_str(self):
        one_cup = self.lookups[1]
        add = one_cup.succ
        ids = []
        while add != one_cup:
            ids.append(add.id)
            add = add.succ
        return ''.join(map(str, ids))

    def mult_ones_succs(self):
        one_cup = self.lookups[1]
        return one_cup.succ.id * one_cup.succ.succ.id
            

cups = list(map(int, list(sys.stdin.read().strip())))
realmax = 1000000
cups += list(range(max(cups) + 1, realmax + 1))
circle = CupCircle(cups)
for _ in range(10000000):
    circle.move()

print(circle.mult_ones_succs())
#print(circle.past_one_str())
