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

from typing import Any, Generator
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


def solve():
    def get_strength(s, two=False):
        if two:
            alpha = "J23456789TQKA"
        else:
            alpha = "23456789TJQKA"
        return [alpha.index(c) for c in s]

    def get_possible(s : str):
        return itertools.product(*["23456789TQKA" if c == "J" else c for c in s])

    def get_type(s, two=False):
        if two: return max(get_type(t, two=False) for t in get_possible(s))
        return sorted(list(Counter(s).values()), reverse=True)

    def get_key(s, two=False):
        return (get_type(s[0], two), get_strength(s[0], two), s[1])

    _data = [(s[0], int(s[1])) for s in [line.split() for line in data]]
    def get_ans(two=False):
        sorted_data = sorted(_data, key=lambda s: get_key(s, two))
        return sum(val * (i + 1) for i, (_, val) in enumerate(sorted_data))

    return (get_ans(False), get_ans(True))


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

