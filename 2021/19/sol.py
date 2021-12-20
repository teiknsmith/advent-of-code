from collections import Counter
import numpy as np
from sys import stdin
import operator as op

INF = float('inf')


def solve():
    scanners = []
    for g in groups():
        scanners.append([np.array([[v] for v in (map(int, l.split(',')))]) for l in g[1:]])

    converted = [False]*len(scanners)
    converted[0] = True
    scanhomes = [None]*len(scanners)
    scanhomes[0] = np.array([[0],[0],[0]])
    pos_rots = [
        np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]]),
        np.array([[0,1,0],
                  [0,0,1],
                  [1,0,0]]),
        np.array([[0,0,1],
                  [1,0,0],
                  [0,1,0]])
    ]
    quart_rots = [
        np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]]),
        np.array([[1,0,0],
                  [0,0,-1],
                  [0,1,0]]),
        np.array([[1,0,0],
                  [0,-1,0],
                  [0,0,-1]]),
        np.array([[1,0,0],
                  [0,0,1],
                  [0,-1,0]]),
    ]
    ud_rots = [
        np.array([[1,0,0],
                  [0,1,0],
                  [0,0,1]]),
        np.array([[-1,0,0],
                  [0,0,1],
                  [0,1,0]]),
    ]
    rots = [np.matmul(p, np.matmul(q, u)) for p in pos_rots for q in quart_rots for u in ud_rots]
    scanrots = [None]*len(scanners)
    scanrots[0] = [[np.matmul(rot, b) for b in scanners[0]] for rot in rots]
    last_converts = [0]
    while not all(converted):
        new_converts = []
        for sci, c in enumerate(converted):
            if c:
                continue

            for refi in last_converts:
                found_match = False
                for roti in range(24):
                    # see if scanners[i] matches with scanners[refi]
                    dtup, nval = max(Counter(map(lambda v: tuple(v.flatten()), (ref - b for ref in scanrots[refi][roti] for b in scanners[sci]))).items(), key=op.itemgetter(1))
                    if nval >= 12:
                        # if so, set scanners
                        dvec = np.array([[d] for d in dtup])
                        scanners[sci] = [ogv + dvec for ogv in scanners[sci]]

                        rvec = np.linalg.inv(rots[roti])
                        scanners[sci] = [np.matmul(rvec, ogv) for ogv in scanners[sci]]

                        scanhomes[sci] = np.matmul(rvec, dvec)
                        

                        # and scanrots
                        scanrots[sci] = [[np.matmul(rot, b) for b in scanners[sci]] for rot in rots]

                        converted[sci] = True
                        new_converts.append(sci)
                        found_match = True
                        break
                if found_match:
                    break
        last_converts = new_converts


    print(len({tuple(v.flatten()) for s in scanners for v in s}))

    maxman = -INF
    for i, h1 in enumerate(scanhomes):
        for h2 in scanhomes[i+1:]:
            maxman = max(maxman, sum(map(abs, h1-h2)))
    print(maxman)



def groups():
    return [g.split('\n') for g in stdin.read().strip().split('\n\n')]




if __name__ == '__main__':
    solve()
