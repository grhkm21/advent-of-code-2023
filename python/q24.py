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
import sympy

from fractions import Fraction
from typing import Any
from colorama import Fore, Style
from sympy.ntheory.modular import crt, solve_congruence
from collections import Counter, deque
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

    def solve_linear(mat, col):
        assert len(mat) == 2 and len(mat[0]) == 2
        det = mat[0][0] * mat[1][1] - mat[0][1] * mat[1][0]
        if det == 0:
            if col[0] * mat[1][0] != col[1] * mat[0][0] or col[0] * mat[1][1] != col[1] * mat[0][1]:
                return None
            return MAX, MAX
        inv = [[mat[1][1], -mat[0][1]], [-mat[1][0], mat[0][0]]]
        t1, t2 = [Fraction(vec[0] * col[0] + vec[1] * col[1], det) for vec in inv]
        if t1 < 0 or t2 < 0:
            return None
        return t1, t2

    vals = [list(map(get_ints, line.split(" @ "))) for line in data]

    n = len(vals)
    for i, j in itertools.combinations(range(n), 2):
        (x1, y1, _), (dx1, dy1, _) = vals[i]
        (x2, y2, _), (dx2, dy2, _) = vals[j]
        mat = [[dx1, -dx2], [dy1, -dy2]]
        col = [x2 - x1, y2 - y1]
        sols = solve_linear(mat, col)
        if sols is None:
            continue

        if sols == (MAX, MAX):
            part1 += 1
            continue

        t1 = sols[0]
        x, y = x1 + dx1 * t1, y1 + dy1 * t1
        if LBOUND <= x <= HBOUND and LBOUND <= y <= HBOUND:
            part1 += 1

    x0, y0, z0, dx0, dy0, dz0 = sympy.var("x0, y0, z0, dx0, dy0, dz0")
    eqs = []
    for (x, y, z), (dx, dy, dz) in sample(vals, 10):
        eqs.append((dx - dx0) * (y0 - y) - (dy - dy0) * (x0 - x))
        eqs.append((dx - dx0) * (z0 - z) - (dz - dz0) * (x0 - x))
        eqs.append((dy - dy0) * (z0 - z) - (dz - dz0) * (y0 - y))

    part2 = sum(sympy.solve(sample(eqs, 10), x0, y0, z0, dx0, dy0, dz0)[0][:3])

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
            raise ValueError(f"The `SUBMIT` environment variable ({submit_arg}) is not an integer.")

        if not (0 <= arg <= 2):
            raise ValueError(f"Invalid `SUBMIT` ({submit_arg}), should be between 0 and 2.")

        part1, part2 = solve()
        part = 2 if arg == 2 or (arg == 0 and part2 != 0) else 1
        ans = part2 if arg == 2 or (arg == 0 and part2 != 0) else part1
        print(f"Submitting {Fore.GREEN}{ans}{Style.RESET_ALL} to day {get_day()} part {part}.")
        submit(part, ans, get_day(), 2023)

    elif time_arg is not None:
        try:
            arg = int(time_arg)
        except ValueError:
            raise ValueError(f"The `TIME` environment variable ({time_arg}) is not an integer.")

        print(f"Timing code for {arg} times!")
        with open(os.devnull, "w") as fout:
            μt = timeit.timeit(lambda: main(file=fout), number=arg) / arg * 10**6
            if μt < 10**3:
                print(f"Time taken: {μt:.2f}μs")
            elif μt < 10**6:
                print(f"Time taken: {μt / 10**3:.2f}ms")
            else:
                print(f"Time taken: {μt / 10**6:.2f}s")
    else:
        main()

