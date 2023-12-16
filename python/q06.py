import glob
import hashlib
import itertools
import json
import multiprocessing as mp
import os
import numpy as np
import re
import string
import sys
import time
import timeit
import datetime

from math import floor, sqrt
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
        lines = fin.read().strip().split("\n")
        # Note: It might include the header "Game ...:" number!
        # lines = [get_ints(line) for line in lines]

    return lines


def solve(data):
    part1 = 1
    part2 = 0

    time = get_ints(data[0])
    dist = get_ints(data[1])

    def _solve(t, d):
        y = floor((t - sqrt(t**2 - 4*d)) / 2) + 1
        return t + 1 - 2 * y

    part1 = prod([_solve(t, d) for t, d in zip(time, dist)])
    part2 = _solve(*map(lambda s: int(''.join(map(str, s))), [time, dist]))
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
            μt = timeit.timeit(lambda: main(file=fout), number=arg) / arg * 10**6
            if μt < 10**3:
                print(f"Time taken: {μt:.2f}μs")
            elif μt < 10**6:
                print(f"Time taken: {μt / 10**3:.2f}ms")
            else:
                print(f"Time taken: {μt / 10**6:.2f}s")
    else:
        main()

