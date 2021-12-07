import sys
from collections import deque as deq
import functools
import math
import numpy as np
import re
e = enumerate

class TileGrid:
    def __init__(self):
        self.flipped = set()
    def selected_tile(self, path):
        tile = [0,0]
        prevc = None
        for c in path:
            if c == 'w' and prevc != 'n':
                tile[0] -= 1
            elif c == 'e' and prevc != 's':
                tile[0] += 1
            elif c == 'n':
                tile[1] += 1
            elif c == 's':
                tile[1] -= 1
            prevc = c
        return tuple(tile)
    def flip(self, path):
        tiletup = self.selected_tile(path)
        if tiletup in self.flipped:
            self.flipped.remove(tiletup)
        else:
            self.flipped.add(tiletup)

    @staticmethod
    def neighbors(x, y):
        return {
            (x-1,y),
            (x,y+1),
            (x+1,y+1),
            (x+1,y),
            (x,y-1),
            (x-1,y-1),
        }
    def next_day(self):
        neighb_counts = dict()
        for tile in self.flipped:
            for neighb in TileGrid.neighbors(*tile):
                if neighb in neighb_counts:
                    neighb_counts[neighb] += 1
                else:
                    neighb_counts[neighb] = 1
        new_flips = {tile for tile, count in neighb_counts.items() if tile not in self.flipped and count == 2}
        unflips = {tile for tile in self.flipped if tile not in neighb_counts or neighb_counts[tile] > 2}
        self.flipped = (self.flipped - unflips).union(new_flips)
            

lines = sys.stdin.readlines()
tiles = TileGrid()
for line in lines:
    tiles.flip(line)
sola = len(tiles.flipped)

for _ in range(100):
    tiles.next_day()

solb = len(tiles.flipped)


print("Part 1: ", sola)

print("Part 2: ", solb)

