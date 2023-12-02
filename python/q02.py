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

    for line in data:
        cur_id = int(line.split(": ")[0].split()[1])
        data = [u.split(", ") for u in line.split(": ")[1].split("; ")]
        cnt = Counter()
        ok = True
        for u in data:
            for v in u:
                a, b = v.split()
                # cnt[b] += int(a)
                if int(a) > {"red": 12, "green": 13, "blue": 14}[b]:
                    ok = False
        if ok:
            ans += cur_id
        # if cnt["blue"] <= 14 and cnt["red"] <= 12 and cnt["green"] <= 13:
        #     ans += cur_id

    return ans


def part2(data):
    ans = 0

    for line in data:
        mn = Counter()
        cur_id = int(line.split(": ")[0].split()[1])
        data = [u.split(", ") for u in line.split(": ")[1].split("; ")]
        cnt = Counter()
        ok = True
        for u in data:
            for v in u:
                a, b = v.split()
                mn[b] = max(mn[b], int(a))
        ans += product(mn.values())

    return ans


if __name__ == "__main__":
    data = parse_data()
    print("[!] part1:", part1(data))
    print("[!] part2:", part2(data))
