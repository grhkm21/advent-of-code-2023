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
from sympy.ntheory.modular import crt
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

    global seq, data
    with open(fname, "r") as fin:
        seq, dt = fin.read().strip().split("\n\n")
        data = dt.split("\n")


def solve():
    part1 = 0
    part2 = MAX

    mp = {}
    for line in data:
        lhs, rhs = line.split(" = ")
        rhs = rhs.strip("(").strip(")")
        mp[lhs] = rhs.split(", ")

    cur = "AAA"
    while cur != "ZZZ":
        ins = seq[part1 % len(seq)]
        cur = mp[cur][ins == "R"]
        part1 += 1

    ok = []
    for s in mp:
        if s[-1] == "A":
            orb = [s]
            for i in range(26**3 * 10):
                ins = seq[i % len(seq)]
                orb.append(mp[orb[-1]][ins == "R"])
            dt = {}
            for i, t in enumerate(orb):
                key = (t, i % 2)
                if key not in dt:
                    dt[key] = []
                dt[key].append(i)
            cur = []
            for key, val in dt.items():
                t = key[0]
                if t[-1] != "Z":
                    continue
                if len(val) == 1:
                    continue
                cur.append((val[-1] - val[-2], val[-1]))
            ok.append(cur)

    for u in itertools.product(*ok):
        mod, rem = [r[0] for r in u], [r[1] for r in u]
        cur = crt(mod, rem)
        if cur is not None and cur[0] != 0:
            part2 = cur[0]

    return (part1, part2)


def main(file=sys.stdout):
    part1, part2 = solve()
    print("[!] part1:", part1, file=file)
    print("[!] part2:", part2, file=file)


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
