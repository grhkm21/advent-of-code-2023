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

    def parse_line(line, part):
        dirs = {"U": (0, 1), "D": (0, -1), "R": (1, 0), "L": (-1, 0)}
        op, dist, color = re.findall(r"([RDLU]) (\d+) \(#(.+)\)", line)[0]
        if part == 1:
            return (dirs[op], int(dist))
        return (dirs["RDLU"[int(color[-1])]], int(color[:5], 16))

    def solve_part(part):
        xs, ys = [], []
        cx, cy = 0, 0
        edges = left = right = 0

        for line1, line2 in zip(data, data[1:] + [data[0]]):
            (dx, dy), dist = parse_line(line1, part)
            (rx, ry), _ = parse_line(line2, part)

            edges += dist - 1
            if (rx, ry) == (dy, -dx):
                right += 1
            elif (rx, ry) == (-dy, dx):
                left += 1

            nx, ny = cx + dist * dx, cy + dist * dy
            xs.append(nx)
            ys.append(ny)
            cx, cy = nx, ny

        ans = sum(ys[i] * (xs[i + 1] - xs[i - 1]) for i in range(len(xs) - 1)) // 2
        ans += (edges * 2 + left * 1 + right * 3) // 4

        return ans

    part1 = solve_part(1)
    part2 = solve_part(2)

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

