import sys

l = sys.stdin.read().split('\n')
l = [int(el) for el in l if el]

for i, el in enumerate(l):
    for el2 in l[i:]:
        if el + el2 == 2020:
            print(el*el2)
