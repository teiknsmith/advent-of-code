import sys

l = sys.stdin.read().split('\n')
l = [int(el) for el in l if el]

for i, el in enumerate(l):
    for j, el2 in enumerate(l[i:]):
        for el3 in l[i+j:]:
            if el + el2 + el3 == 2020:
                print(el*el2*el3)
