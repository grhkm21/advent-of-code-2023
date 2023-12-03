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
        j = 0
        while j < m:
            if data[i][j] not in string.digits:
                j += 1
                continue
            cur_str = ""
            ok = False
            while j < m and data[i][j] in string.digits:
                cur_str += data[i][j]
                if any(pos in symbols for pos in adj4(i, j)):
                    ok = True
                j += 1
            if ok:
                print(cur_str)
                ans += int(cur_str)
            else:
                print("not ok", cur_str)

    return ans


def part2(data):
    ans = 0

    n, m = len(data), len(data[0])
    symbols = set()
    mp = {}
    for i in range(n):
        for j in range(m):
            if data[i][j] not in '.' + string.digits:
                symbols.add((i, j))
                if data[i][j] == '*':
                    mp[i, j] = []

    for i in range(n):
        j = 0
        while j < m:
            if data[i][j] not in string.digits:
                j += 1
                continue
            cur_str = ""
            ok = False
            ok2 = set()
            while j < m and data[i][j] in string.digits:
                cur_str += data[i][j]
                for pos in adj4(i, j):
                    if pos in symbols:
                        ok = True
                        if pos in mp:
                            ok2.add(pos)
                j += 1
            if ok:
                for pos in ok2:
                    mp[pos].append(int(cur_str))

    for key in mp:
        if len(mp[key]) >= 2:
            assert len(mp[key]) == 2
            print(key, mp[key])
            ans += product(mp[key])

    return ans


if __name__ == "__main__":
    data = parse_data()
    print("[!] part1:", part1(data))
    print("[!] part2:", part2(data))
