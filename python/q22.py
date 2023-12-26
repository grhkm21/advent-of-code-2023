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
import copy

from typing import Any
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
        data = []
        for line in fin.read().strip().split("\n"):
            a, b = map(lambda s: list(map(int, s.split(","))), line.split("~"))
            data.append((a, b))


def solve():
    part1 = 0
    part2 = 0

    def make_piece(p, q):
        return list(itertools.product(*map(lambda r: range(r[0], r[1] + 1), map(sorted, zip(p, q)))))

    def drop(piece):
        return [(x, y, z - 1) for x, y, z in piece]

    pieces = [make_piece(a, b) for a, b in data]
    assert all((0, 0, 0) <= p < (10, 10, 300) for piece in pieces for p in piece)

    grid = np.zeros((10, 10, 300), dtype=int)
    for pos in itertools.product(range(10), range(10), range(300)):
        grid[pos] = -1

    for i, piece in enumerate(pieces):
        for p in piece:
            grid[p] = i

    while True:
        flag = False
        for i, piece in enumerate(pieces):
            for p in piece:
                grid[p] = -1
            new_piece = drop(piece)
            if all(p[2] >= 1 for p in new_piece) and all(grid[p] == -1 for p in new_piece):
                flag = True
                pieces[i] = new_piece
            for p in pieces[i]:
                grid[p] = i
        if not flag:
            break

    dt = []
    rev = defaultdict(set)
    for i, piece in enumerate(pieces):
        new_piece = drop(piece)
        cur = set()
        for j, p in enumerate(new_piece):
            if p[2] >= 1 and grid[p] != -1 and grid[p] != i:
                cur.add(grid[p])
                rev[grid[p]].add(i)
        dt.append(cur)

    for i in range(len(pieces)):
        for j in range(len(pieces)):
            if j == i:
                continue
            if len(dt[j]) == 1 and i in dt[j]:
                break
        else:
            part1 += 1

    def dfs(v):
        nonlocal gone
        gone.add(v)
        for u in rev[v]:
            if all(d in gone for d in dt[u]):
                dfs(u)

    for v in range(len(pieces)):
        gone = set()
        dfs(v)
        # print(v, gone)
        part2 += len(gone) - 1

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

