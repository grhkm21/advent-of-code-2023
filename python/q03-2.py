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
from collections import Counter, deque
from functools import reduce, cache
from random import random, randrange, randint
from tqdm import tqdm, trange
from util import *

def parse_data():
    if len(sys.argv) == 1:
        qno = __file__.split("/")[-1]
        if qno == "template.py":
            raise RuntimeError("The code does not work for template.py :)")
        else:
            fname = "../input/in_2023_" + qno[1:3]
    elif len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        raise RuntimeError(f"Usage: {sys.argv[0]} [input]")

    global data
    with open(fname, "r") as fin:
        data = fin.read().strip().split("\n")
        data = list(map(list, data))


def get_nums(filtered):
    nums = sum([re.findall(r"\d+", "".join(row)) for row in filtered], [])
    return list(map(int, nums))


def part1():
    filtered = [["."] * len(data[i]) for i in range(len(data))]
    vis = set()
    dq = deque()

    r, c = len(data), len(data[0])
    is_valid = lambda pos: 0 <= pos[0] < r and 0 <= pos[1] < c

    for pos in itertools.product(range(r), range(c)):
        if is_valid(pos) and data[pos[0]][pos[1]] not in string.digits + ".":
            dq.append(pos)
            vis.add(pos)

    while len(dq) > 0:
        i, j = dq.pop()
        filtered[i][j] = data[i][j]
        for pos in filter(is_valid, adj8(i, j)):
            if data[pos[0]][pos[1]] in string.digits and pos not in vis:
                dq.append(pos)
                vis.add(pos)

    return sum(get_nums(filtered))


def part2():
    ans = 0

    r, c = len(data), len(data[0])

    vis = set()
    is_valid = lambda pos: 0 <= pos[0] < r and 0 <= pos[1] < c

    def dfs(i, j):
        nonlocal vis, filtered
        vis.add((i, j))
        filtered[i][j] = data[i][j]
        for i, j in filter(is_valid, adj8(i, j)):
            if data[i][j] in string.digits and (i, j) not in vis:
                dfs(i, j)

    for i in range(r):
        for j in range(c):
            if data[i][j] == "*":
                filtered = [["."] * c for _ in range(r)]
                dfs(i, j)
                nums = get_nums(filtered)
                if len(nums) >= 2:
                    ans += product(nums)

    return ans


def main(file=sys.stdout):
    print("[!] part1:", part1(), file=file)
    print("[!] part2:", part2(), file=file)


if __name__ == "__main__":
    parse_data()
    arg = os.environ.get("TIME")

    if arg is not None:
        try:
            arg = int(arg)
        except ValueError:
            raise ValueError(f"The `TIME` environment variable ({arg}) is not an integer.")

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

