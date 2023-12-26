import copy
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
import networkx as nx

from typing import Any
from colorama import Fore, Style
from sympy.ntheory.modular import crt, solve_congruence
from collections import Counter, defaultdict, deque
from functools import reduce, cache
from random import choice, random, randrange, randint
from tqdm import tqdm, trange
from util import *

sys.setrecursionlimit(10**5)


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

    graph1 = defaultdict(dict)
    graph2 = defaultdict(dict)
    r, c = len(data), len(data[0])

    START = (0, data[0].index("."))
    END = (r - 1, data[r - 1].index("."))

    is_valid = lambda x, y: 0 <= x < r and 0 <= y < c and data[x][y] != "#"
    ndir_dict = {">": [(0, 1)], "<": [(0, -1)], "^": [(-1, 0)], "v": [(1, 0)], ".": list(adj4(0, 0))}

    for i, j in itertools.product(range(r), range(c)):
        if data[i][j] == "#":
            continue

        for ndir in ndir_dict[data[i][j]]:
            x, y = i + ndir[0], j + ndir[1]
            if is_valid(x, y):
                graph1[i, j][x, y] = 1
                if data[x][y] == ".":
                    graph1[x, y][i, j] = 1

        for x, y in adj4(i, j):
            if is_valid(x, y):
                graph2[i, j][x, y] = 1
                graph2[x, y][i, j] = 1

    while True:
        for u in graph2:
            if len(graph2[u]) == 2:
                left, right = list(graph2[u].keys())
                weight = sum(graph2[u].values())
                graph2[left][right] = weight
                graph2[right][left] = weight
                del graph2[u]
                del graph2[left][u]
                del graph2[right][u]
                break
        else:
            break

    def solve_graph(graph):
        # Reindex graph vertices
        keys = {y: x for x, y in enumerate(graph.keys())}
        graph = {keys[u]: {keys[v]: graph[u][v] for v in graph[u]} for u in graph}

        ans = 0
        _START, _END = keys[START], keys[END]
        dq = deque()

        dq.append((_START, 1 << _START, 0))
        while len(dq) > 0:
            u, vis, dist = dq.pop()
            if u == _END:
                ans = max(ans, dist)
                continue
            while len(d := graph[u]) == 1:
                u, dt = list(d.items())[0]
                if (vis >> u) & 1:
                    break
                vis |= 1 << u
                dist += dt
            else:
                for v, dt in d.items():
                    if (vis >> v) & 1:
                        continue
                    dq.append((v, vis | (1 << v), dist + dt))

        return ans

    part1 = solve_graph(graph1)
    part2 = solve_graph(graph2)

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

