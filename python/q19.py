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

    global rules, data
    with open(fname, "r") as fin:
        crules, data = [s.split("\n") for s in fin.read().strip().split("\n\n")]
        rules = {line.split("{")[0]: line.split("{")[1].rstrip("}").split(",") for line in crules}


def solve():
    part1 = 0
    part2 = 0

    def process(dt, key):
        for rule in rules[key]:
            if ":" in rule:
                cond, target = rule.split(":")
                assert "<" in cond or ">" in cond, f"{cond} {target}"
                cond = eval(str(dt[cond[0]]) + cond[1:])
            else:
                cond, target = True, rule
            if cond:
                if target == "R" or target == "A":
                    return target == "A"
                return process(dt, target)
        raise RuntimeError(f"Unreachable? {dt} {key}")

    def update_bounds(name, op, val, bounds):
        nbounds = dict(bounds)
        lb, hb = bounds[name]
        if op == ">":
            lb = max(lb, val + 1)
        else:
            hb = min(hb, val - 1)
        nbounds[name] = (lb, hb)
        return nbounds

    def negate_rule(op, val):
        if op == ">":
            return ("<", val + 1)
        return (">", val - 1)

    def dfs(key, bounds):
        # print(f"dfs({key}, {bounds})")
        if any(val[1] < val[0] for val in bounds.values()):
            return 0
        if key == "R":
            return 0
        if key == "A":
           return product(val[1] - val[0] + 1 for val in bounds.values())
        res = 0
        pat = re.compile(r"([xmas])([<>])(\d+):(.+)")
        for rule in rules[key]:
            if ":" in rule:
                name, op, val, target = pat.findall(rule)[0]
                val = int(val)
                res += dfs(target, update_bounds(name, op, val, bounds))
                bounds = update_bounds(name, *negate_rule(op, val), bounds)
            else:
                res += dfs(rule, bounds)
        return res

    for line in data:
        dt = {key: int(val) for key, val in re.findall(r"(.)=(\d+)", line)}
        res = process(dt, "in")
        if res:
            part1 += sum(dt.values())
    part2 = dfs("in", {key: (1, 4000) for key in "xmas"})

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

