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
    qno = __file__.split("/")[-1]

    if qno == "template.py":
        raise RuntimeError("The code does not work for template.py :)")

    qno = qno[1:3]
    with open(f"../input/in_2023_{qno}", "r") as fin:
        lines = fin.read().strip().split("\n")

    pass

    return lines


def part1(data):
    ans = 0

    n, m = len(data), len(data[0])
    symbols = set()
    for i in range(n):
        for j in range(m):
            if data[i][j] not in '.' + string.digits:
                symbols.add((i, j))

    for i in range(n):
        for match in re.finditer(r"\d+", data[i]):
            start, end, num = match.start(), match.end(), match.group()
            if any(pos in symbols for j in range(start, end) for pos in adj8(i, j)):
                ans += int(num)

    return ans


def part2(data):
    ans = 0

    n, m = len(data), len(data[0])
    mp = {}
    for i in range(n):
        for j in range(m):
            if data[i][j] == '*':
                mp[i, j] = []

    for i in range(n):
        for match in re.finditer(r"\d+", data[i]):
            start, end, num = match.start(), match.end(), int(match.group())
            added = set()
            for j in range(start, end):
                for pos in adj8(i, j):
                    if pos in mp and pos not in added:
                        added.add(pos)
                        mp[pos].append(num)

    for val in mp.values():
        if len(val) >= 2:
            ans += product(val)

    return ans


if __name__ == "__main__":
    data = parse_data()
    print("[!] part1:", part1(data))
    print("[!] part2:", part2(data))
