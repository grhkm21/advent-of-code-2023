import glob
import copy
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

    keys = set()
    flip_flops = {}
    conjugators = {}
    broadcast = []
    graph = defaultdict(list)
    rev_graph = defaultdict(list)
    data.sort(reverse=True)

    for line in data:
        key, val = line.split(" -> ")
        key = key.lstrip("%").lstrip("&")
        val = val.split(", ")
        graph[key] = val
        for v in val:
            rev_graph[v].append(key)

        keys.add(key)
        for k in val:
            keys.add(k)

        if line.startswith("broadcaster"):
            broadcast = val
        elif line.startswith("%"):
            flip_flops[key] = val
        else:
            dt = {"broadcaster": False} if key in broadcast else {}
            conjugators[key] = (val, dt)

    for key in keys:
        vals = flip_flops[key] if key in flip_flops else conjugators[key][0] if key in conjugators else broadcast
        for val in vals:
            if val in conjugators:
                conjugators[val][1][key] = False

    def dump_graph():
        arr = []
        for key in flip_flops.keys():
            arr.append(f"{key}[color=\"red\" style=\"filled\"]")
        for key in conjugators.keys():
            arr.append(f"{key}[fillcolor=\"green\" style=\"filled\"]")
        for key in graph:
            for val in graph[key]:
                arr.append(f"{key}->{val}")
        with open("/tmp/a","w") as fout:
            fout.write("digraph{"+";".join(arr)+"}")

    def process(dq : Deque[Tuple[str, bool, str]], cyc : int):
        nonlocal states, conj_states, ans, low, high
        while len(dq) > 0:
            head, state, prev = dq.popleft()
            # print(f"{prev=} -> {head=} : state={'False' if not state else 'HIGH'}")
            if cyc <= 1000:
                if state == False:
                    low += 1
                else:
                    high += 1

            if head == "broadcaster":
                for dest in broadcast:
                    dq.append((dest, state, head))
            elif head in flip_flops:
                if state == False:
                    states[head] = not states[head]
                    for dest in flip_flops[head]:
                        dq.append((dest, states[head], head))
            elif head in conjugators:
                conj_states[head][prev] = state
                out = not all(conj_states[head].values())
                for dest in conjugators[head][0]:
                    dq.append((dest, out, head))

            if not state and head in rev_graph["jz"] and head not in ans:
                ans[head] = cyc

    ans = Counter()
    states = {key: False for key in keys if key not in conjugators}
    conj_states = {key: dict(conjugators[key][1]) for key in conjugators}
    low, high = 0, 0
    ans = Counter()

    cyc = 1
    while any(key not in ans for key in rev_graph["jz"]):
        process(deque([("broadcaster", False, "button")]), cyc)
        cyc += 1

    part1 = low * high
    part2 = product(ans.values())

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

