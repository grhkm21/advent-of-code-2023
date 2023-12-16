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
        data = [list(s) for s in fin.read().strip().split("\n")]


def solve():
    part1 = 0
    part2 = 0

    def to_north(grid):
        data = [list(row) for row in grid]
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == "O":
                    # roll north
                    k = i
                    while k > 0 and data[k - 1][j] == ".":
                        data[k - 1][j], data[k][j] = data[k][j], data[k - 1][j]
                        k -= 1
        return data

    def tilt(grid):
        grid = to_north(grid)
        grid = transpose(to_north(transpose(grid)))
        grid = rot180(to_north(rot180(grid)))
        grid = rot180(transpose(to_north(transpose(rot180(grid)))))
        return grid

    def score(grid):
        ans = 0
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] == "O":
                    ans += len(grid) - i
        return ans

    part1 = score(to_north(data))

    _hash = lambda grid: ";".join("".join(row) for row in grid)
    mp = {}
    grid = [list(row) for row in data]
    TARGET = 1000000000
    for t in range(1, 1000):
        if part2 != 0:
            break
        grid = tilt(grid)
        key = _hash(grid)
        if key not in mp:
            mp[key] = []
        mp[key].append(t)
        if len(mp[key]) > 10:
            cyc = mp[key][-1] - mp[key][-2]
            if TARGET % cyc == t % cyc:
                print("!", t, TARGET, cyc, mp[key])
                part2 = score(grid)

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

