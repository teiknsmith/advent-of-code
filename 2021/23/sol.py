import typing
from sys import stdin
from collections import defaultdict, Counter
from copy import copy, deepcopy
import itertools as ittls
import heapq as q

INF = float('inf')


class State:
    cmap = defaultdict(lambda: '.', ((ord(c) - ord('A'), c) for c in "ABCD"))

    def __init__(self, sthgt, stacks, hallway, sc, minsc, cmplts, par) -> None:
        self.stack_height = sthgt
        self.stacks = stacks
        self.hallway = hallway
        self.score = sc
        self.minscoreleft = minsc
        self.completes = cmplts
        self.parent = par

    def all_here(self):
        cs = Counter(ittls.chain(self.hallway, *self.stacks))
        return all(cs[k] == 2 for k in range(4))

    def __str__(self) -> str:
        ls = ["#" * 13 + f'  sc: {self.score}', \
              '#' + ''.join(self.cmap[c] for c in self.hallway) + f'#  minleft: {self.minscoreleft}']
        head, end = '###', '##'
        for i in range(self.stack_height - 1, -1, -1):
            newl = [head]
            for st in self.stacks:
                try:
                    newl.append(self.cmap[st[i]])
                except IndexError:
                    newl.append(self.cmap[None])
                newl.append('#')
            newl.append(end)
            ls.append(''.join(newl))
            head, end = '  #', '  '
        ls.append('  #########  ')
        return '\n'.join(ls)

    def minscore(self):
        return self.score + self.minscoreleft

    def complete(self):
        return all(self.completes)

    @classmethod
    def from_listy(cls, listy):
        positions = deepcopy(listy)
        score = 0
        minscore = 0

        downfillds = [len(positions[0])] * 4
        for i, st in enumerate(positions):
            mustmove = False
            for j, el in enumerate(st):
                if not mustmove and el == i:
                    downfillds[i] -= 1
                    continue
                mustmove = True
                steps = 0

                # to top
                steps += len(st) - j
                # then across
                if el == i:
                    steps += 2
                else:
                    steps += 2 * abs(el - i)

                minscore += steps * (10**el)
        for v in downfillds:
            minscore += (v**2 + v) // 2

        return cls(len(positions[0]), positions, [None] * 11, score, minscore,
                   [False] * len(positions), None)

    @staticmethod
    def c_to_h(cidx):
        return 2 * (cidx + 1)

    def chln(self) -> typing.List['State']:
        res = []
        for curr_hidx, el in enumerate(self.hallway):
            if el is None:
                continue
            home_hidx = self.c_to_h(el)
            home_is_ready = all(hel == el for hel in self.stacks[el])
            hall_is_clear = curr_hidx < home_hidx and all(
                self.hallway[h] is None
                for h in range(curr_hidx + 1, home_hidx + 1))
            hall_is_clear |= curr_hidx > home_hidx and all(
                self.hallway[h] is None
                for h in range(curr_hidx - 1, home_hidx - 1, -1))
            if home_is_ready and hall_is_clear:
                newhall = copy(self.hallway)
                newhall[curr_hidx] = None

                newstacks = deepcopy(self.stacks)

                newcomplts = copy(self.completes)

                steps = abs(home_hidx - curr_hidx)
                steps += self.stack_height - len(newstacks[el])
                newstacks[el].append(el)

                scadd = steps * (10**el)

                iscmpl = len(newstacks[el]) == self.stack_height
                newcomplts[el] = iscmpl

                res.append(
                    State(self.stack_height, newstacks, newhall,
                          self.score + scadd, self.minscoreleft - scadd,
                          newcomplts, self))

                # don't bother adding to hallway if we can clear it out a lil.
                # if there are more ready, we'll see it next time.
                return res
        for i, st in enumerate(self.stacks):
            if all(el == i for el in st):
                continue
            curr_hidx = self.c_to_h(i)
            el = st[-1]
            home_hidx = self.c_to_h(el)
            home_is_ready = all(hel == el for hel in self.stacks[el])
            hall_is_clear = curr_hidx < home_hidx and all(
                self.hallway[h] is None
                for h in range(curr_hidx, home_hidx + 1))
            hall_is_clear |= curr_hidx > home_hidx and all(
                self.hallway[h] is None
                for h in range(curr_hidx, home_hidx - 1, -1))
            if home_is_ready and hall_is_clear:

                newhall = copy(self.hallway)

                newstacks = deepcopy(self.stacks)
                newstacks[i].pop()

                newcomplts = copy(self.completes)

                steps = self.stack_height - len(newstacks[i])
                steps += abs(home_hidx - curr_hidx)
                steps += self.stack_height - len(newstacks[el])
                newstacks[el].append(el)

                scadd = steps * (10**el)

                iscmpl = len(newstacks[el]) == self.stack_height
                newcomplts[el] = iscmpl

                res.append(
                    State(self.stack_height, newstacks, newhall,
                          self.score + scadd, self.minscoreleft - scadd,
                          newcomplts, self))

                # don't bother putting it in the hallway if we can send it home
                continue

            for stepdir, stop, extra in [(1, len(self.hallway), len(self.hallway) - 1), \
                                          (-1, 0, 0)]:
                for newhidx in list(
                        range(curr_hidx + stepdir, stop,
                              2 * stepdir)) + [extra]:
                    if self.hallway[newhidx] is not None:
                        break

                    newhall = copy(self.hallway)
                    newhall[newhidx] = el

                    newstacks = deepcopy(self.stacks)
                    el = newstacks[i].pop()

                    newcomplts = copy(self.completes)

                    vsteps = self.stack_height - len(newstacks[i])
                    hsteps = abs(newhidx - curr_hidx)

                    vscadd = vsteps * (10**el)
                    hscadd = hsteps * (10**el)
                    newsc = self.score + vscadd + hscadd

                    newminsc = self.minscoreleft - vscadd
                    delta_home_dist = abs(home_hidx -
                                          newhidx) - abs(home_hidx - curr_hidx)
                    newminsc += delta_home_dist * (10**el)

                    res.append(
                        State(self.stack_height, newstacks, newhall, newsc,
                              newminsc, newcomplts, self))
        return res


def solve():
    ls = lines()
    stcks = [[] for _ in range(4)]
    for r in range(-2, -6, -1):
        for i in range(4):
            stcks[i].append(ord(ls[r][3 + 2 * i]) - ord('A'))

    print(list(map(len, stcks)))
    uniq = 0
    st = State.from_listy(stcks)
    sts = [(st.minscoreleft, uniq, st)]
    uniq += 1

    bssf = INF
    while sts:
        minsc, _, st = q.heappop(sts)
        if st.complete() and st.score < bssf:
            bssf = st.score
            continue
        if minsc > bssf:
            continue
        for newst in st.chln():
            if newst.minscore() < bssf:
                q.heappush(sts, (newst.minscoreleft, uniq, newst))
                uniq += 1

    print(bssf)


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
