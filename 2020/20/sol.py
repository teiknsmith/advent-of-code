import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
e = enumerate

class Tile:
    def __init__(self, text):
        lines = text.strip().split('\n')
        self.tid = int(lines[0].split()[1][:-1])
        self.grid = np.array(list(map(list, lines[1:])))
        self.sides = [[self.grid[0], self.grid[:,-1], self.grid[-1][::-1], self.grid[:,0][::-1]], [self.grid[:,0], self.grid[-1], self.grid[:,-1][::-1], self.grid[0][::-1]]]
        self.rot(0)
    def rot(self, rotnum):
        self.cwidx, self.ridx = rotnum // 4, rotnum % 4
        return self
    def uside(self):
        return self.sides[self.cwidx][self.ridx]
    def rside(self):
        return self.sides[self.cwidx][(self.ridx + 1) % 4]        
    def dside(self):
        return self.sides[self.cwidx][(self.ridx + 2) % 4]        
    def lside(self):
        return self.sides[self.cwidx][(self.ridx + 3) % 4]        
    def compatible(self, lneighb, uneighb):
        return (((not lneighb)
                 or np.array_equal(self.lside()[::-1], lneighb.rside()))
                and
                ((not uneighb)
                 or np.array_equal(self.uside()[::-1], uneighb.dside()))
               )
    
tiles = list(map(Tile, sys.stdin.read().split('\n\n')))

class PartialSol:
    @staticmethod
    def root(tiles):
        res = PartialSol()
        res.tiles = tiles
        res.side_len = int(math.sqrt(len(tiles)))
        res.unused = set(range(len(tiles)))
        res.used = []
        return res
    @staticmethod
    def from_parent(parent, newtidx, newrot):
        res = PartialSol()
        res.tiles = parent.tiles
        res.side_len = parent.side_len
        res.unused = parent.unused - {newtidx}
        res.used = parent.used + [(newtidx, newrot)]
        return res
    def corner_prod(self):
        if not self.is_solution():
            return 0
        ul = self.used[0]
        ur = self.used[self.side_len - 1]
        dl = self.used[-self.side_len]
        dr = self.used[-1]
        return functools.reduce(lambda acc, el: acc * el,
                                [self.tiles[idx[0]].tid for idx in
                                 [ul, ur, dl, dr]],
                                1)
    def children(self):
        if not self.unused:
            return []
        res = []
        uneighb, lneighb = None, None
        if len(self.used) >= self.side_len:
            uidx, urot = self.used[-self.side_len]
            uneighb = tiles[uidx].rot(urot)
        if len(self.used) % self.side_len != 0:
            lidx, lrot = self.used[-1]
            lneighb = tiles[lidx].rot(lrot)
        for tidx in self.unused:
            for rot in range(8):
                if tiles[tidx].rot(rot).compatible(lneighb, uneighb):
                    res.append(PartialSol.from_parent(self, tidx, rot))
        return res
    def solutions(self, accum=None):
        if accum is None:
            accum = set()
        if self.is_solution():
            accum.add(self)
        else:
            for child in self.children():
                child.solutions(accum)
        return accum
    def is_solution(self):
        return not self.unused
        
for sol in PartialSol.root(tiles).solutions():
    break

sola = sol.corner_prod()

def unpadded_tile(tile):
    return tile.grid[1:-1,1:-1]
def rotated_tile(tile, rot_num):
    ccw, turns = rot_num // 4, rot_num % 4
    res = tile.copy()
    if ccw:
        res = res.T
    if turns:
        res = np.rot90(res, turns)
    return res

side_len = sol.side_len
imbits = [rotated_tile(unpadded_tile(tiles[idx]), rot) for idx, rot in sol.used]
np.core.arrayprint._line_width = 100
im = functools.reduce(
      lambda acc, el: np.append(acc, el, 0),
      (functools.reduce((lambda acc, el: np.append(acc, el, 1)),
                       imbits[beg:beg+side_len])
                        for beg in range(0,len(imbits), side_len)))

monstertxt = (
"                  # \n"
"#    ##    ##    ###\n"
" #  #  #  #  #  #   ")
monster = np.array(list(map(list, monstertxt.split('\n'))))

def matches_subim(im, i, j, subim):
    subh, subw = subim.shape
    imh, imw = im.shape
    if i + subh > imh or j + subw > imw:
        return False
    imslice = im[i:i+subh, j:j+subw]
    return all(spx == ' ' or ipx == '#' for ipx, spx in zip(imslice.flatten(), subim.flatten()))

def num_subims(im, subim):
    h, w = im.shape
    return len([1 for i in range(h) for j in range(w) if matches_subim(im, i, j, monster)])

nmonsters = 0
for rot in range(8):
    nmonsters = num_subims(im, monster)
    if nmonsters:
        break
    im = np.rot90(im)
    if rot == 3:
        im = im.T

solb = (im == '#').sum() - (monster == '#').sum() * nmonsters


print("Part 1: ", sola)

print("Part 2: ", solb)

