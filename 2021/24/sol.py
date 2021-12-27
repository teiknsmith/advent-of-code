from collections import deque
import numpy as np
from sys import stdin
import functools as fntls
import itertools as ittls
import operator as op
import subprocess

INF = float('inf')

OPS = {
    "add": op.add,
    "mul": op.mul,
    "div": op.floordiv,
    "mod": op.mod,
    "eql": lambda a, b: int(a == b),
}

OPSTRS = {
    "add": '+',
    "mul": '*',
    "div": '//',
    "mod": '%',
    "eql": '==',
}
COPSTRS = {
    "add": '+',
    "mul": '*',
    "div": '/',
    "mod": '%',
    "eql": '==',
}


def solve():
    prog = lines()

    mem = runprog(prog, None)
    finexpr = mem['z']

    # finexpr.draw_graph()

    # print()
    # print()
    cfunc = finexpr.cfunc()
    print(cfunc)
    print()
    # return
    cprog = f"""\
#include "stdio.h"

{cfunc}

int main() {{
    int vals[14];
    for (int i = 0; i < 14; ++i) {{
        vals[i] = 9;
    }}
    
    int ii = 0;
    int evaled = 0;
    int finished = 0;
    while (!finished) {{
        ii += 1;
        
        evaled = monad(vals);
        if (!evaled) {{
            printf("solution! ");
            for (int i = 0; i < 14; ++i) {{
                printf("%d", vals[i]);
            }}
            printf("\\n");
            break;
        }}
        if (!(ii%1000000)) {{
            for (int i = 0; i < 14; ++i) {{
                printf("%d", vals[i]);
            }}
            printf(" --> %d\\n", evaled);
        }}
        for (int i = 14-1; i >= 0; --i) {{
            vals[i] -= 1;
            if (vals[i] == 0) {{
                if (i == 0) {{
                    finished = 1;
                }}
                vals[i] = 9;
            }} else {{
                break;
            }}
        }}
    }}
    return 0;
}}
"""

    with open('monad.c', 'w') as monadout:
        monadout.write(cprog)

    subprocess.run(['gcc', '-o', 'monad.out', 'monad.c'])
    subprocess.run('./monad.out')

    return

    invars = list(reversed(Var.allvars))
    vals = [9] * len(invars)

    ii = 0
    while True:
        ii += 1

        # could be list, yeah?vvvvv faster? do we know? do we care?
        evaled = finexpr.eval(tuple(zip(invars, vals)))
        if not evaled:
            print('solution!', ''.join(map(str, reversed(vals))))
        if not ii % 10000:
            print(''.join(map(str, reversed(vals))), ' --> ', evaled)

        for i, val in enumerate(vals):
            vals[i] = val - 1
            if vals[i] == 0:
                vals[i] = 9
            else:
                break
        else:
            break

    return

    for model_num in range(9**14 - 1, -1, -1):
        if not runprog(
                prog,
                iter(
                    list(map(lambda c: int(c) + 1, np.base_repr(model_num,
                                                                9)))))['z']:
            print(''.join(
                map(lambda c: str(int(c) + 1), np.base_repr(model_num, 9))))
            break


class Expr:
    def __init__(self, l, o, r) -> None:
        self.l: 'Expr' = l
        self.o: str = o
        self.r: 'Expr' = r
        self.used_vars: set = self.l.used_vars.union(self.r.used_vars)

        self.incount = 0
        self.accum_c_seen_id = None

    def _mark_ins(self):
        tosee = deque([self])
        seen = set()
        while tosee:
            u = tosee.popleft()
            if u in seen:
                continue
            u.accum_c_seen_id = None
            seen.add(u)
            if type(u) is Expr:
                u.l.incount += 1
                u.r.incount += 1
                tosee.append(u.l)
                tosee.append(u.r)

    def _accum_clines(self, res):
        if self.accum_c_seen_id is not None:
            return f'v{self.accum_c_seen_id}'

        lstr = self.l._accum_clines(res)
        rstr = self.r._accum_clines(res)
        mystr = f'({lstr} {COPSTRS[self.o]} {rstr})'

        self.accum_c_seen_id = Expr.next_accum_c_seen_id
        Expr.next_accum_c_seen_id += 1

        if self.incount > 1:
            res.append(f'  int v{self.accum_c_seen_id} = {mystr};')
            return f'v{self.accum_c_seen_id}'
        else:
            return mystr

    def cfunc(self):
        res = ["int monad(int *d) {"]
        Expr.next_accum_c_seen_id = 0
        self._mark_ins()

        finexpr = self._accum_clines(res)
        res.append(f'  return {finexpr};')
        res.append('}')
        return '\n'.join(res)

    @classmethod
    def from_bits(cls, l: 'Expr', o, r: 'Expr'):
        lval = l.value()
        rval = r.value()

        if isinstance(lval, int) and isinstance(rval, int):
            return Literal(OPS[o](lval, rval))

        # for symmetric reductions
        for a, b, aval, bval in [(l, r, lval, rval), (r, l, rval, lval)]:
            if isinstance(aval, int):
                if aval == 0:
                    if o == 'add':
                        return bval
                    elif o == 'mul':
                        return Literal(0)
                if aval == 1 and o == 'mul':
                    return bval
                if o == 'mul' and type(bval) is Expr and bval.o == 'add':
                    if isinstance(bval.l, Literal) or isinstance(
                            bval.r, Literal):
                        newl = cls.from_bits(bval.l, 'mul', a)
                        newr = cls.from_bits(bval.r, 'mul', a)
                        return cls.from_bits(newl, 'add', newr)
                if o == 'add' and type(bval) is Expr and bval.o == 'add':
                    for subl, subr in [(bval.l, bval.r), (bval.r, bval.l)]:
                        if isinstance(subl, Literal):
                            newlit = Literal(aval + subl.value())
                            newoth = subr
                            return cls.from_bits(newoth, 'add', newlit)
            if type(aval) is Expr and type(bval) is Expr:
                if o == aval.o and o == bval.o:
                    if o == 'add':
                        for bsubl, bsubr in [(bval.l, bval.r),
                                             (bval.r, bval.l)]:
                            if isinstance(bsubl, Literal):
                                for asubl, asubr in [(aval.l, aval.r),
                                                     (aval.r, aval.l)]:
                                    if isinstance(asubl, Literal):
                                        newlit = Literal(bsubl.value() +
                                                         asubl.value())
                                        newoth = cls.from_bits(
                                            asubr, 'add', bsubr)
                                        return cls.from_bits(
                                            newoth, 'add', newlit)

        if isinstance(lval, int):
            if lval == 0:
                if o in ['div', 'mod']:
                    return Literal(0)
        if isinstance(rval, int):
            if rval == 0:
                if o in ['div', 'mod']:
                    raise ZeroDivisionError()
            if rval == 1:
                if o == 'div':
                    return lval
                elif o == 'mod':
                    return Literal(0)

        if o == 'eql':
            lmin, lmax = l.valrange
            rmin, rmax = r.valrange
            if rmax < lmin or lmax < rmin:
                return Literal(0)

        # if isinstance(rval, int) and o == 'mod' and type(lval) is Expr:
        #     if lval.o == 'add':
        #         newl = cls.from_bits(lval)

        return cls(l, o, r)

    def value(self):
        return self

    @fntls.cached_property
    def valrange(self):
        if self.o == 'eql':
            return 0, 1
        rmin, rmax = self.r.valrange
        if self.o == 'mod':
            return 0, rmax - 1
        lmin, lmax = self.l.valrange
        if self.o == 'add':
            return lmin + rmin, lmax + rmax

        # don't want to think through negatives, just brute all options
        lvals = [lmin, lmax]
        if lmin < 0 < lmax:
            lvals.append(0)
            if 1 < lmax:
                lvals.append(1)
            if lmin < -1:
                lvals.append(-1)
        rvals = [rmin, rmax]
        if rmin < 0 < rmax:
            rvals.append(0)
            if 1 < rmax:
                rvals.append(1)
            if rmin < -1:
                rvals.append(-1)
        if self.o == 'mul':
            vs = list(ittls.starmap(op.mul, ittls.product(lvals, rvals)))
            return min(vs), max(vs)
        elif self.o == 'div':
            # don't want to think through negatives, just brute all options
            vs = list(
                v
                for v in ittls.starmap(lambda l, r: None if not r else l // r,
                                       ittls.product(lvals, rvals))
                if v is not None)
            return min(vs), max(vs)

    @fntls.lru_cache(maxsize=None)
    def _truval(self, var_bindings):
        lval = self.l.eval(var_bindings)
        rval = self.r.eval(var_bindings)
        return OPS[self.o](lval, rval)

    def eval(self, var_bindings):
        rel_vars = tuple(
            (var, val) for var, val in var_bindings if var in self.used_vars)
        return self._truval(rel_vars)

    def draw_graph(self):
        with open('monad.graph', 'w') as gout:
            gout.write(self.graph_str())
        subprocess.run(['graph-easy', 'monad.graph'])

    def graph_str(self):
        res = ['strict digraph expr {']
        self.__accum_graph_str(res)
        res.append('}')

        seenls = set()
        seenadd = seenls.add
        res = [l for l in res if not (l in seenls or seenadd(l))]
        return '\n'.join(res)

    def _graph_label(self):
        return OPSTRS[self.o]  #+ ' (' + str(self.valrange) + ')'

    def __accum_graph_str(self, res):
        res.append(f'  {id(self)} [label="{self._graph_label()}"];')
        if type(self) is Expr:
            res.append(f'  {id(self)} -> {id(self.l)};')
            res.append(f'  {id(self)} -> {id(self.r)};')
            self.l.__accum_graph_str(res)
            self.r.__accum_graph_str(res)

    def __str__(self) -> str:
        return f'({self.l.value()} {OPSTRS[self.o]} {self.r.value()})'

    def __repr__(self) -> str:
        return str(self)


class Var(Expr):
    nextvar = 0
    allvars = []

    def __init__(self) -> None:
        self.var_id = f'd{Var.nextvar}'
        Var.nextvar += 1
        Var.allvars.append(self)
        self.used_vars = {self}
        self.incount = 0

    def _truval(self, bindings):
        assert len(bindings) == 1
        print(f"checking with {self.var_id}, giving {bindings[0][1]}")
        return bindings[0][1]

    def value(self):
        return self

    @fntls.cached_property
    def valrange(self):
        return 1, 9

    def _graph_label(self):
        return str(self)

    def __str__(self) -> str:
        return self.var_id

    def _accum_clines(self, _):
        return f'd[{self.var_id[1:]}]'


class Literal(Expr):
    def __init__(self, v) -> None:
        self.v = v
        self.used_vars = set()
        self.incount = 0

    def eval(self, _):
        return self.v

    def value(self):
        return self.v

    @fntls.cached_property
    def valrange(self):
        return self.v, self.v

    def _graph_label(self):
        return str(self)

    def __str__(self) -> str:
        return str(self.v)

    def _accum_clines(self, _):
        return str(self)


def runprog(prog, prog_inp):
    mem = {k: Literal(0) for k in "wxyz"}

    for l in prog:
        parms = l.split()
        if parms[0] == "inp":
            mem[parms[1]] = Var()
        else:
            try:
                v = Literal(int(parms[2]))
            except:
                v = mem[parms[2]]

            a = mem[parms[1]]
            mem[parms[1]] = Expr.from_bits(a, parms[0], v)

    return mem


def lines():
    return stdin.read().strip().split('\n')


if __name__ == '__main__':
    solve()
