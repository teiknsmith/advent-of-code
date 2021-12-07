import numpy as np
import sys

def evolve(state):
    padded = np.pad(state, 2, mode='constant')
    res = padded.copy()

    d0, d1, d2, d3 = np.shape(res)
    for i in range(1,d0-1):
        for j in range(1,d1-1):
            for k in range(1,d2-1):
                for w in range(1,d3-1):
                    me = padded[i,j,k,w]
                    num_neighbs = sum(
                        padded[i-1:i+2,j-1:j+2,k-1:k+2,w-1:w+2].flatten()
                    ) - me
                    if me and not num_neighbs in [2,3]:
                        res[i,j,k,w] = 0
                    elif not me and num_neighbs == 3:
                        res[i,j,k,w] = 1
    return res
                
grid = np.array([[[[1 if el == '#' else 0 for el in l.strip()] for l in sys.stdin.readlines()]]])

for _ in range(6):
    grid = evolve(grid)

print(np.sum(grid))
