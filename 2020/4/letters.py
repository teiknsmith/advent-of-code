import sys

inlet = sys.stdin.read()
letcs = dict()

for c in inlet:
    if c in letcs:
        letcs[c] += 1
    else:
        letcs[c] = 1

for c, count in letcs.items():
    print(f"{c}: {count}")
