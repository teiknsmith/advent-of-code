import sys

def sid(ps):
    l = 0
    h = 127
    adj = 64
    for c in ps[:7]:
        if c == 'F':
            h -= adj
        else:
            l += adj
        #print(f"{l,h}")
        adj /= 2
    row = l
    #print(row)
    l = 0
    h = 8
    adj = 4
    for c in ps[7:-1]:
        if c == 'L':
            h -= adj
        else:
            l += adj
        #print(f"{l,h}")
        adj /= 2
    col = l
    #print(col)
    return row * 8 + col
    

l = sys.stdin.readlines()
l = [sid(line) for line in l if line.strip()]

l = sorted(l)
for a, b in zip(l[:-1], l[1:]):
    if b - a == 2:
        print(a + 1)

