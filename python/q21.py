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
import sympy.abc

from fractions import Fraction
from typing import Any, Deque, Tuple
from colorama import Fore, Style
from sympy.ntheory.modular import crt, solve_congruence
from collections import Counter, defaultdict, deque
from functools import reduce, cache
from random import random, randrange, randint
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

    r, c = len(data), len(data[0])
    assert r == c

    sx, sy = 0, 0
    dq = deque()
    for i, j in itertools.product(range(r), range(c)):
        if data[i][j] == "S":
            sx, sy = i, j
            dq.append((sx, sy, 0))
            break
    else:
        raise RuntimeError("S not found")

    target = 5000
    offset = target % r

    vis = set([(sx, sy)])
    dist = {}
    while len(dq) > 0:
        x, y, d = dq.popleft()
        dist[x, y] = d
        if d > offset + 5 * r:
            continue
        for nx, ny in adj4(x, y):
            if (nx, ny) not in vis and data[nx % r][ny % c] != "#":
                vis.add((nx, ny))
                dq.append((nx, ny, d + 1))

    def get_val(st):
        return len([dist[x, y] for x, y in dist if dist[x, y] <= st and dist[x, y] % 2 == st % 2])

    def interpolate(xs, f, nx):
        n = len(xs)
        ys = [f(x) for x in xs]
        res = 0
        for i in range(n):
            cur = product((sympy.abc.x - xs[j]) / (xs[i] - xs[j]) for j in range(n) if j != i)
            res += cur * ys[i]
        return res.subs({sympy.abc.x: nx})

    part1 = get_val(64)
    part2 = interpolate(range(3), lambda x: get_val(offset + r * x), target // r)

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

