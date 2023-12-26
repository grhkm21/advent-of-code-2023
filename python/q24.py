import glob
import hashlib
import itertools
import json
import math
import multiprocessing as mp
import os
import numpy as np
import re
import string
import sys
import time
import timeit
import datetime

from fractions import Fraction
from typing import Any
from colorama import Fore, Style
from sympy.ntheory.modular import crt, solve_congruence
from collections import Counter, defaultdict, deque
from functools import reduce, cache
from random import random, randrange, randint, sample
from tqdm import tqdm, trange
from util import *


def get_day():
    qno = __file__.split("/")[-1]
    if qno == "template.py":
        raise RuntimeError("Don't run template.py :)")
    return int(qno[1:3])


def parse_data():
    if len(sys.argv) == 1:
        fname = f"../input/in_2023_{get_day()}"
    elif len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        raise RuntimeError(f"Usage: {sys.argv[0]} [input_file]")

    global data
    with open(fname, "r") as fin:
        data = fin.read().strip().split("\n")


def solve():
    part1 = 0
    part2 = 0

    LBOUND = 200000000000000
    HBOUND = 400000000000000

    # LBOUND, HBOUND = 7, 27

    def row_reduce(mat, vec):
        nrows = len(mat)
        ncols = len(mat[0])

        # We form the block matrix [mat | vec] instead
        for i in range(nrows):
            mat[i].append(vec[i])
            mat[i] = list(map(Fraction, mat[i]))

        nncols = len(mat[0])
        pivots = []
        row, col = 0, 0
        while row < nrows and col < ncols:
            # pivot row
            prow = row
            while prow < nrows and mat[prow][col] == 0:
                prow += 1
            if prow == nrows:
                col += 1
                continue
            pivots.append(col)
            # swap mat[row] with mat[prow]
            if row != prow:
                mat[row], mat[prow] = mat[prow], mat[row]
            # normalise row
            for col_ in reversed(range(col, nncols)):
                mat[row][col_] /= mat[row][col]
            # subtract all subsequent rows
            for row_ in range(row + 1, nrows):
                for col_ in reversed(range(col, nncols)):
                    mat[row_][col_] -= mat[row_][col] * mat[row][col_]
            row += 1

        if any(mat[row][-1] != 0 for row in range(len(pivots), nrows)):
            raise RuntimeError("no solution")

        # back substitute, returns *any* solution if non-full rank
        sols = [[0]] * ncols
        for prow, pcol in reversed(list(enumerate(pivots))):
            for row in range(prow):
                for col in reversed(range(pcol, nncols)):
                    mat[row][col] -= mat[prow][col] * mat[row][pcol]
            sols[pcol] = mat[prow][ncols:]

        return [sol for (sol,) in sols]

    assert row_reduce([[1, 3, 1], [2, 6, 2], [1, 3, 2]], vec=[2, 4,
                                                              7]) == [-3, 0, 5]
    assert row_reduce([[1, 0], [0, 1], [1, 2]], vec=[3, 5, 13]) == [3, 5]

    vals = [list(map(get_ints, line.split(" @ "))) for line in data]

    class Monomial:

        def __init__(self, mons):
            assert isinstance(mons, list)
            self.mons = sorted(mons)

        def __mul__(self, other):
            assert isinstance(other, Monomial)
            return Monomial(self.mons + other.mons)

        def __hash__(self):
            if len(self.mons) == 0:
                return hash(1)
            return hash(tuple(self.mons))

        def __eq__(self, other):
            if isinstance(other, int):
                return other == 1 and len(self.mons) == 0
            if isinstance(other, Expr):
                return Expr(self) == other
            assert isinstance(other, Monomial)
            return self.mons == other.mons

        def __repr__(self):
            if len(self.mons) == 0:
                return "1"
            return "*".join(self.mons)

    class Expr:

        dt: Counter[Monomial | int]

        def __init__(self, dt):
            if isinstance(dt, int):
                self.dt = Counter({Monomial([]): dt})
                return
            if isinstance(dt, str):
                self.dt = Counter({Monomial([dt]): 1})
                return
            if isinstance(dt, Monomial):
                self.dt = Counter({dt: 1})
                return
            if isinstance(dt, dict):
                dt = Counter(dt)
            assert isinstance(dt, Counter)
            self.dt = dt

        def __add__(self, other):
            if not isinstance(other, Expr):
                other = Expr(other)

            dt = Counter(self.dt)
            for key, val in other.dt.items():
                dt[key] += val
            return Expr(dt)

        def __radd__(self, other):
            return self + other

        def __getitem__(self, key):
            return self.dt[key]

        def __iter__(self):
            return iter(self.dt)

        def __mul__(self, other):
            if isinstance(other, int):
                return self * Expr(other)

            return Expr({
                key1 * key2: self[key1] * other[key2] for key1 in self
                for key2 in other
            })

        def __rmul__(self, other):
            return self * other

        def __neg__(self):
            return Expr({key: -val for key, val in self.dt.items()})

        def __sub__(self, other):
            return self + (-other)

        def __rsub__(self, other):
            return (-self) + other

        def __eq__(self, other):
            return self.dt == other.dt

        def _get_str(self, data):
            s, c = data
            s = str(s)
            if s == "1":
                return str(c)
            if c == 1:
                return s
            if c == -1:
                return "-" + s
            return f"{c}*{s}"

        def __repr__(self):
            if len(self.dt) == 0:
                return "0"
            self.reduce()
            items = sorted(list(self.items()), key=lambda it: str(it[0]))
            return " + ".join(map(self._get_str, items))

        def __hash__(self):
            self.reduce()
            if len(self.dt) == 1 and list(self.dt.values()) == [1]:
                return hash(list(self.dt.keys())[0])
            return hash(str(self))

        def reduce(self):
            self.dt = Counter({
                key: val for key, val in self.dt.items() if val != 0
            })
            return self

        def items(self):
            return self.dt.items()

        def const(self):
            return self.dt[1]

        def split_const(self):
            return self.const(), (self - self.const()).reduce()

    def var(s):
        return Expr(s.strip())

    def varlist(s):
        return list(map(var, s.split(",")))

    def linearize(eqs):
        # Setup coefficient matrix
        mons = {}
        mons_list = []
        sparse_mat = []
        col_vec = []
        for term in eqs:
            row = {}
            const, non_const = term.split_const()
            col_vec.append(-const)
            for mon, coef in non_const.items():
                if mon not in mons:
                    mons[mon] = len(mons)
                    mons_list.append(mon)
                row[mons[mon]] = coef
            sparse_mat.append(row)

        # Create dense matrix again
        mat = [[0] * len(mons) for _ in range(len(sparse_mat))]
        for i, row in enumerate(sparse_mat):
            for j, v in row.items():
                mat[i][j] = v

        return dict(zip(mons_list, row_reduce(mat, col_vec)))

    #################### PART 1 ####################
    n = len(vals)
    t1, t2 = varlist("t1, t2")
    for i, j in itertools.combinations(range(n), 2):
        (x1, y1, _), (dx1, dy1, _) = vals[i]
        (x2, y2, _), (dx2, dy2, _) = vals[j]
        eqs = [(x1 + t1 * dx1) - (x2 + t2 * dx2), (y1 + t1 * dy1) - (y2 + t2 * dy2)]
        try:
            sols = linearize(eqs)
        except RuntimeError:
            continue

        tt1, tt2 = sols[t1], sols[t2]
        if tt1 < 0 or tt2 < 0:
            continue

        x, y = x1 + dx1 * tt1, y1 + dy1 * tt1
        if LBOUND <= x <= HBOUND and LBOUND <= y <= HBOUND:
            part1 += 1

    #################### PART 2 ####################
    eqs = []
    x0, y0, z0, dx0, dy0, dz0 = varlist("x0, y0, z0, dx0, dy0, dz0")
    for (x, y, z), (dx, dy, dz) in sample(vals, 30):
        eqs.append((dx - dx0) * (y0 - y) - (dy - dy0) * (x0 - x))
        eqs.append((dx - dx0) * (z0 - z) - (dz - dz0) * (x0 - x))
        eqs.append((dy - dy0) * (z0 - z) - (dz - dz0) * (y0 - y))

    sol = linearize(eqs)
    part2 = sol[x0] + sol[y0] + sol[z0]

    return (part1, part2)


def main(file=sys.stdout):
    part1, part2 = solve()
    print("[!] part1:", part1, file=file)
    print("[!] part2:", part2, file=file)


if __name__ == "__main__":
    parse_data()
    time_arg = os.environ.get("TIME")
    submit_arg = os.environ.get("SUBMIT")

    if submit_arg is not None:
        from submit import submit
        try:
            arg = int(submit_arg)
        except ValueError:
            raise ValueError(
                f"The `SUBMIT` environment variable ({submit_arg}) is not an integer."
            )

        if not (0 <= arg <= 2):
            raise ValueError(
                f"Invalid `SUBMIT` ({submit_arg}), should be between 0 and 2.")

        part1, part2 = solve()
        part = 2 if arg == 2 or (arg == 0 and part2 != 0) else 1
        ans = part2 if arg == 2 or (arg == 0 and part2 != 0) else part1
        print(
            f"Submitting {Fore.GREEN}{ans}{Style.RESET_ALL} to day {get_day()} part {part}."
        )
        submit(part, ans, get_day(), 2023)

    elif time_arg is not None:
        try:
            arg = int(time_arg)
        except ValueError:
            raise ValueError(
                f"The `TIME` environment variable ({time_arg}) is not an integer."
            )

        print(f"Timing code for {arg} times!")
        with open(os.devnull, "w") as fout:
            μt = timeit.timeit(lambda: main(file=fout),
                               number=arg) / arg * 10**6
            if μt < 10**3:
                print(f"Time taken: {μt:.2f}μs")
            elif μt < 10**6:
                print(f"Time taken: {μt / 10**3:.2f}ms")
            else:
                print(f"Time taken: {μt / 10**6:.2f}s")
    else:
        main()
