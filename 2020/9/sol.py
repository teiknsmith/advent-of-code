import sys
from collections import deque as deq

B = 25

lines = [int(l) for l in sys.stdin.readlines()]
active = deq(maxlen=B)

for n in lines:
    if len(active) == B:
        good = False
        for ela in active:
            for elb in active:
                if ela + elb == n and ela != elb:
                    good = True
                    break
            if good:
                break
        if not good:
            bad = n
    active.append(n)

for i, n in enumerate(lines):
    #print("test ", n)
    s = n
    used = {n}
    for nb in lines[i+1:]:
        #print("    ", nb)
        s += nb
        used.add(nb)
        if s == bad:
            l = min(used)
            h = max(used)
            print(l + h)
        elif s > bad:
            break
        
        
