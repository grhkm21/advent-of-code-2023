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

    line = data[0].split(",")
    def _hash(s):
        cur = 0
        for c in s:
            cur = (cur + ord(c)) * 17 % 256
        return cur

    for s in line:
        part1 += _hash(s)

    boxes = [[] for _ in range(256)]
    for s in line:
        a, op, b = re.findall(r"(.+)([-=])(.?)", s)[0]
        key = _hash(a)
        # print(a, key)
        if op == "-":
            val = [s for s in boxes[key] if s[0] == a]
            if len(val) > 0:
                boxes[key].remove(val[0])
        elif op == "=":
            for i in range(len(boxes[key])):
                if boxes[key][i][0] == a:
                    boxes[key][i] = (a, int(b))
                    break
            else:
                boxes[key].append((a, int(b)))
    for i in range(len(boxes)):
        for j in range(len(boxes[i])):
            part2 += (i + 1) * (j + 1) * boxes[i][j][1]

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

