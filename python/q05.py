import glob
import hashlib
import itertools
import json
import math
import multiprocessing as mp
import numpy as np
import re
import string
import sys
import time

from collections import Counter
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

    assert len(maps[0]) == 1
    orig = list(map(int, maps[0][0].split()))

    @cache
    def follow(val):
        path = []
        for block in maps[1:]:
            for i, rg in enumerate(block):
                dest, src, length = list(map(int, rg.split()))
                if src <= val < src + length:
                    val = dest + (val - src)
                    path.append(i)
                    break
        return val, path

    part1 = min(map(follow, orig))[0]

    # part 2 - binary search for spots where the "path" followed changes
    def search(start, end):
        if end < start:
            return None

        mid = (start + end) // 2
        val_start = follow(start)
        val_mid = follow(mid)
        val_end = follow(end)
        if val_start[1] == val_end[1]:
            return val_start[0]

        if end == start + 1:
            return val_end[0]

        ans = 10**100
        if val_start[1] != val_mid[1]:
            ans = min(ans, search(start, mid))

        if val_mid[1] != val_end[1]:
            ans = min(ans, search(mid, end))

        return ans

    for i in range(0, len(orig), 2):
        start, length = orig[i], orig[i + 1]
        range_ans = search(start, start + length - 1)
        part2 = min(part2, range_ans)

    return (part1, part2)


if __name__ == "__main__":
    data = parse_data()
    part1, part2 = solve(data)
    print("[!] part1:", part1)
    print("[!] part2:", part2)
