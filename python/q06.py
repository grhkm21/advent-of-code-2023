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
        lines = fin.read().strip().split("\n")
        # Note: It might include the header "Game ...:" number!
        # lines = [get_ints(line) for line in lines]

    return lines


def solve(data):
    part1 = 1
    part2 = 0

    time = get_ints(data[0])
    dist = get_ints(data[1])

    for t, d in zip(time, dist):
        cnt = 0
        for j in range(t + 1):
            if j * (t - j) > d:
                cnt += 1
        part1 *= cnt

    t, d = map(lambda s: int(''.join(map(str, s))), [time, dist])
    for j in trange(t + 1):
        part2 += j * (t - j) > d

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
