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

    m, n = len(data), len(data[0])
    is_valid = lambda pos: 0 <= pos[0] < m and 0 <= pos[1] < n

    def bfs_dq(st):
        dq = deque([st])
        vis = set([st[0]])
        vis_dir = set([st])

        while len(dq) > 0:
            pos, dirc = dq.popleft()
            (x, y), (dx, dy) = pos, dirc
            assert is_valid(pos)

            c = data[x][y]
            ndirs = []

            if c == "/":
                ndirs.append((-dy, -dx))
            elif c == "\\":
                ndirs.append((dy, dx))
            elif c == "|" and dx == 0:
                ndirs.append((1, 0))
                ndirs.append((-1, 0))
            elif c == "-" and dy == 0:
                ndirs.append((0, -1))
                ndirs.append((0, 1))
            else:
                ndirs.append(dirc)

            for nx, ny in ndirs:
                npos = (x + nx, y + ny)
                ndata = (npos, (nx, ny))
                if not is_valid(npos) or ndata in vis_dir:
                    continue
                vis.add(npos)
                vis_dir.add(ndata)
                dq.append(ndata)

        return len(vis)

    poss = []
    for r in range(m):
        poss.append(((r, 0), (0, 1)))
        poss.append(((r, n - 1), (0, -1)))
    for c in range(n):
        poss.append(((0, c), (1, 0)))
        poss.append(((m - 1, c), (-1, 0)))

    part1 = bfs_dq(poss[0])
    part2 = max(map(bfs_dq, poss))

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

