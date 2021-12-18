import numpy as np
from sys import stdin
from collections import deque, defaultdict
from copy import copy
import functools as fntls
import itertools as ittls
import operator as op
import math
import re
import string
import heapq as q

INF = float('inf')

class FishNum:
    def __init__(self, l, r, d):
        self.l = l
        self.r = r
        self.d = d
        if FishNum.constructing and isinstance(self, RegNum):
            self.prev = FishNum.leaf_tail
            if FishNum.leaf_head is None:
                FishNum.leaf_head = self
                FishNum.leaf_tail = self
            FishNum.leaf_tail.next = self
            FishNum.leaf_tail = self
            self.next = None
    
    @classmethod
    def _from_str(cls, s):
        cls.constructing = True
        cls.leaf_head = None
        cls.leaf_tail = None
        res, _ = cls.__from_str(s, 0, 0)
        cls.constructing = False
        return res, cls.leaf_head, cls.leaf_tail

    @classmethod
    def __from_str(cls, s: str, si, d):
        if s[si].isdigit():
            ei = si
            while s[ei].isdigit():
                ei += 1
            return RegNum(int(s[si:ei]), d), ei

        left, ei = cls.__from_str(s, si+1, d+1)
        right, ei = cls.__from_str(s, ei+1, d+1)
        res = cls(left, right, d)
        left.p = res
        right.p = res
        return res, ei+1


    def __str__(self) -> str:
        return ''.join(self._str(0))

    def _str(self, d):
        return [' '*d, f'[{id(self)}\n'] + self.l._str(d+1) + ['\n'] + self.r._str(d+1)

    def mag(self):
        return 3*self.l.mag() + 2*self.r.mag()

class RegNum(FishNum):
    def __init__(self, v, d):
        self.v = v
        super().__init__(None, None, d)
    def mag(self):
        return self.v
    def _str(self, d):
        return [' '*self.d, str(self.v)]

class FishTree:
    adds = 0
    class Null:
        def __iadd__(self, r):
            return r
    def __init__(self, s):
        self.root, self.head, self.tail = FishNum._from_str(s)
    def mag(self):
        return self.root.mag()
    def __iadd__(self, r: 'FishTree'):
        FishTree.adds += 1
        doprint = False
        if FishTree.adds >= 5:
            doprint = True
        self.tail.next = r.head
        r.head.prev = self.tail
        self.tail = r.tail
        self.root = FishNum(self.root, r.root, 0)
        self.root.l.p = self.root
        self.root.r.p = self.root
        sc = self.head
        # doprint = 0
        while sc:
            sc.d += 1
            # if sc.d == 4:
            #     doprint = 20
            # print(sc.d, id(sc), id(sc.next))
            sc = sc.next

        changed = True
        while changed:
            changed = False
            # do explodes, set changed if so
            sc = self.head
            while sc:
                if sc.d >= 5:
                    changed = True
                    toleft, left, right, toright = sc.prev, sc, sc.next, sc.next.next
                    newnode = RegNum(0, sc.d-1)
                    newnode.prev = toleft
                    newnode.next = toright
                    gpa = left.p.p
                    newnode.p = gpa
                    if gpa.l is left.p:
                        gpa.l = newnode
                    else:
                        gpa.r = newnode
                    if toleft:
                        toleft.v += left.v
                        toleft.next = newnode
                    else:
                        self.head = newnode
                    if toright:
                        toright.v += right.v
                        toright.prev = newnode
                    else:
                        self.tail = newnode
                    sc = newnode
                sc = sc.next
                
            # do splits, set changed and immediately continue if newd >= 5
            sc = self.head
            while sc:
                if sc.v >= 10:
                    changed = True
                    l = RegNum(sc.v//2, sc.d+1)
                    r = RegNum(sc.v - sc.v//2, sc.d+1)
                    l.next = r
                    r.prev = l
                    newnode = FishNum(l, r, 0)
                    newnode.p = sc.p
                    l.p = newnode
                    r.p = newnode
                    pa = sc.p
                    if sc is pa.l:
                        pa.l = newnode
                    else:
                        pa.r = newnode
                    left, right = sc.prev, sc.next
                    l.prev = left
                    r.next = right
                    if left:
                        left.next = l
                    else:
                        self.head = l
                    if right:
                        right.prev = r
                    else:
                        self.tail = r
                    if sc.d >= 4:
                        break
                    if l.v >= 10:
                        sc = l
                    elif r.v >= 10:
                        sc = r
                    else:
                        sc = sc.next
                else:
                    sc = sc.next

        return self
    def __str__(self):
        # sc = self.head
        # while sc:
        #     print(sc)
        #     sc = sc.next
        return str(self.root)
    


def solve():
    res = FishTree.Null()
    strs = lines()
    maxmag = -INF
    for i, s0 in enumerate(strs):
        for j, s1 in enumerate(strs):
            if i == j:
                continue
            n = FishTree(s0)
            n += FishTree(s1)
            maxmag = max(maxmag, n.mag())
    print(maxmag)


def lines():
    return stdin.read().strip().split('\n')


def intgridin():
    return [[int(c) for c in r] for r in lines()]


def groups():
    return [g.split('\n') for g in stdin.read().strip().split('\n\n')]


def btwn(v, l, h):
    return (v > l and v < h) or (v < l and v > h)


def btwne(v, l, h):
    return (v >= l and v <= h) or (v <= l and v >= h)


def btwni(v, l, h):
    return v >= l and v < h


def valids(ijl, hii, hij):
    for i, j in ijl:
        if (btwni(i, -INF if hii == INF else 0, hii)
                and btwni(j, -INF if hii == INF else 0, hij)):
            yield (i, j)


def neigh4(i, j, hii=INF, hij=INF):
    yield from valids([(i - 1, j), \
                        (i + 1, j), \
                        (i, j - 1), \
                        (i, j + 1)], hii, hij)


def neigh8(i, j, hii=INF, hij=INF):
    yield from neigh4(i, j, hii, hij)
    yield from valids([(i - 1, j - 1), \
                        (i - 1, j + 1), \
                        (i + 1, j - 1), \
                        (i + 1, j + 1)], hii, hij)


if __name__ == '__main__':
    solve()
