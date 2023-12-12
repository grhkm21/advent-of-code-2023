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

from typing import Any
from colorama import Fore, Style
from sympy.ntheory.modular import crt, solve_congruence
from collections import Counter, deque
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

    G = {}
    chars = "|-LJ7F.S"

    def is_valid(pos, bounds=None):
        if bounds is None:
            return 0 <= pos[0] < len(data) and 0 <= pos[1] < len(data[pos[0]])
        return 0 <= pos[0] < bounds[0] and 0 <= pos[1] < bounds[1]

    def connect(pos1, pos2):
        if not (is_valid(pos1) and is_valid(pos2)):
            return
        nonlocal G
        if pos1 not in G: G[pos1] = []
        if pos2 not in G: G[pos2] = []
        G[pos1].append(pos2)

    start = None
    for i in range(len(data)):
        for j in range(len(data[i])):
            c = data[i][j]
            if c == "S": start = (i, j)
            if c == chars[0]: dest = [(i - 1, j), (i + 1, j)]
            elif c == chars[1]: dest = [(i, j + 1), (i, j - 1)]
            elif c == chars[2]: dest = [(i - 1, j), (i, j + 1)]
            elif c == chars[3]: dest = [(i - 1, j), (i, j - 1)]
            elif c == chars[4]: dest = [(i + 1, j), (i, j - 1)]
            elif c == chars[5]: dest = [(i + 1, j), (i, j + 1)]
            elif c == chars[7]: dest = list(adj4(i, j))
            else: continue
            for pos in dest:
                connect((i, j), pos)

    assert start is not None

    G = {u: [v for v in G[u] if u in G[v]] for u in G}

    vis = set()
    dq1 = deque([(start, [start])])
    loop = None
    while len(dq1) > 0:
        u, path = dq1.pop()
        if u in vis:
            continue
        vis.add(u)
        for v in G[u]:
            if v not in vis:
                dq1.append((v, path + [v]))
            elif v == start and len(path) > 2:
                loop = path

    dist = {}
    vis = set([start])
    dq2 = deque()
    dq2.append((start, 0))
    while len(dq2) > 0:
        u, d = dq2.popleft()
        dist[u] = min(d, dist.get(u, 10**100))
        for v in G[u]:
            if v not in vis:
                vis.add(v)
                dq2.append((v, d + 1))

    assert loop is not None
    part1 = max(dist[v] for v in loop)

    grid = [["."] * (len(data[0]) * 2 - 1) for _ in range(len(data) * 2 - 1)]
    for i in range(len(loop)):
        (x1, y1), (x2, y2) = loop[i - 1], loop[i]
        grid[2 * x1][2 * y1] = "X"
        grid[x1 + x2][y1 + y2] = "X"
    grid = pad(grid)

    vis = set()
    dq3 = deque()
    dq3.append((0, 0))
    while len(dq3) > 0:
        pos = dq3.popleft()
        grid[pos[0]][pos[1]] = "X"
        vis.add(pos)
        for npos in adj4(*pos):
            if npos not in vis and is_valid(npos, (len(grid), len(grid[0]))) and grid[npos[0]][npos[1]] in "#.":
                vis.add(npos)
                dq3.append(npos)

    grid = [row[1::2] for row in grid[1::2]]
    part2 = sum(grid, []).count(".")

    with open("out", "w") as fout:
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                fout.write(grid[i][j])
            fout.write("\n")

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

