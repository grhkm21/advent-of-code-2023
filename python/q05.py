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

from colorama import Fore, Style
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
        qno = __file__.split("/")[-1]
        if qno == "template.py":
            raise RuntimeError("The code does not work for template.py :)")
        else:
            fname = "../input/in_2023_" + qno[1:3]
    elif len(sys.argv) == 2:
        fname = sys.argv[1]
    else:
        raise RuntimeError(f"Usage: {sys.argv[0]} [input]")

    with open(fname, "r") as fin:
        lines = fin.read().strip().split("\n\n")

    return lines


def solve(data):
    part1 = 0
    part2 = 10**100

    maps = [block.split(":")[1].strip().split("\n") for block in data]
    maps = [[list(map(int, val.split())) for val in mp] for mp in maps]

    assert len(maps[0]) == 1
    orig, maps = maps[0][0], [sorted(mp, key=lambda u: u[1]) for mp in maps[1:]]

    def follow(val):
        for block in maps:
            for dest, src, length in block:
                if src <= val < src + length:
                    val = dest + (val - src)
                    break
        return val

    part1 = min(map(follow, orig))

    dq = [(orig[i], orig[i] + orig[i + 1] - 1) for i in range(0, len(orig), 2)]
    for block in maps:
        new_dq = []
        dq.reverse()
        while len(dq) > 0:
            start, end = dq.pop()
            if start < block[0][1]:
                new_dq.append((start, block[0][1] - 1))
                start = block[0][1]
            for dest, src, length in block:
                if end < start:
                    break
                if src <= start < src + length:
                    if end < src + length:
                        new_dq.append((dest + start - src, dest + end - src))
                        break
                    else:
                        new_dq.append((dest + start - src, dest + length - 1))
                        start = src + length
            else:
                if end >= start:
                    new_dq.append((start, end))

        dq = list(new_dq)

    part2 = min(start for start, _ in dq)

    return (part1, part2)


def main(file=sys.stdout):
    part1, part2 = solve(data)
    print("[!] part1:", part1, file=file)
    print("[!] part2:", part2, file=file)


if __name__ == "__main__":
    data = parse_data()
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

        part1, part2 = solve(data)
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

