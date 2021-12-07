import sys
import re
import functools

lines = sys.stdin.readlines()

innard_patt = re.compile(r'(\d+) (.+) bags?')
def stoinnard(s):
    num, name = innard_patt.match(s).groups()
    return (int(num), name)
    

g = dict()
for line in lines:
    outer, innerlist = line.split(" bags contain ")
    inners = innerlist.split(", ")
    inners[-1] = inners[-1].split(".")[0]

    try:
        if inners[0] == 'no other bags':
            inners = []
        else:
            inners = [stoinnard(inner) for inner in inners]
    except:
        print(inners)
    g[outer] = inners

@functools.lru_cache(maxsize=None)
def can_hold(outer, goal):
    if outer == goal:
        return True
    if outer not in g:
        return False
    return any(can_hold(inner[1], goal) for inner in g[outer])

@functools.lru_cache(maxsize=None)
def num_inside(outer):
    return sum(num * (1 + num_inside(inner)) for num, inner in g[outer])

spesh = 'shiny gold'
print(len([holder for holder in g if can_hold(holder, spesh)]) - (1 if spesh in g else 0))
print(num_inside(spesh))
