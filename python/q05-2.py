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
    global data
    data = parse_data()
    arg = os.environ.get("TIME")

    if arg is not None:
        try:
            arg = int(arg)
        except ValueError:
            raise ValueError(f"The `TIME` environment variable ({arg}) is not an integer.")

        print(f"Timing code for {arg} times!")
        with open(os.devnull, "w") as fout:
            t = timeit.timeit(lambda: main(file=fout), number=arg) / arg
            print(f"Time taken: {t}")
    else:
        main()
