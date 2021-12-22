from collections import Counter
import itertools as ittls

# PART 1
# WIN = 1000

# def gendiegen():
# return det_die()

# PART 2
WIN = 21


def gendiegen():
    return dirac()


# the rest
def det_die():
    return ittls.cycle([[v] for v in range(1, 101)])


def dirac():
    while True:
        yield range(1, 4)


def solve():
    p1 = int(input().split(':')[1]) - 1
    p2 = int(input().split(':')[1]) - 1

    wins = [0, 0]
    sts = Counter({(p1, p2, 0, 0): 1})

    diegen = gendiegen()

    part_1 = None
    i = -1
    while sts:
        i += 1
        newsts = Counter()

        player = int(i % 6 >= 3)
        for st in sts:
            newst = list(st)
            for d in next(diegen):
                new_pos = (st[player] + d) % 10
                new_sc = st[player + 2]
                if i % 3 == 2:
                    new_sc += new_pos + 1
                if new_sc >= WIN:
                    wins[player] += sts[st]
                    part_1 = (i + 1) * st[1 - player + 2]
                else:
                    newst[player] = new_pos
                    newst[player + 2] = new_sc
                    newsts[tuple(newst)] += sts[st]

        sts = newsts

    print(part_1)
    print(max(wins))


if __name__ == '__main__':
    solve()
