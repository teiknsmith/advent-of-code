import sys

lines = sys.stdin.readlines()
currs = set()
s = 0
n = True
for l in lines:
    cs = l.strip()
    if cs:
        mids = set(cs)
        if n:
            currs = mids
            n = False
        else:
            currs = currs.intersection(mids)
    else:
        s += len(currs)
        #print(currs)
        currs = set()
        n = True
s += len(currs)
print(currs)
currs = set()
                

print(s)
