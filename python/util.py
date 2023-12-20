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

from operator import add, mul
from collections import Counter
from functools import reduce, cache
from random import random, randrange, randint
from tqdm import tqdm, trange

try:
    import gmpy2
    from gmpy2.gmpy2 import mpz
except ModuleNotFoundError:
    pass


def average(arr):
    arr = list(arr)
    return sum(arr) / len(arr)


def product(arr):
    return reduce(mul, arr)


def adj4(x, y):
    yield (x - 1, y)
    yield (x + 1, y)
    yield (x, y - 1)
    yield (x, y + 1)


def adj8(x, y):
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            if dx == dy == 0:
                continue
            yield (x + dx, y + dy)


def powerset(arr):
    if len(arr) == 0:
        yield []
        return

    u = powerset(arr[1:])
    for s in u:
        yield s
        yield [arr[0]] + s


def revmap(mp):
    res = {}
    for key, val in mp.items():
        if val not in res:
            res[val] = []
        res[val].append(key)
    return res


def get_ints(s):
    return list(map(int, re.findall(r"\d+", s)))


def pad(grid, c="#"):
    c = len(grid[0])
    return [["#"] * (c + 2)] + [["#"] + s + ["#"] for s in grid] + [["#"] * (c + 2)]


def transpose(arr):
    return [[arr[i][j] for i in range(len(arr))] for j in range(len(arr[0]))]


def rot180(arr):
    return [[arr[-i - 1][-j - 1] for j in range(len(arr[0]))] for i in range(len(arr))]


def dist_euclidean(d1, d2):
    return sum((x - y)**2 for x, y in zip(d1, d2))**0.5


def dist_manhattan(d1, d2):
    return sum(abs(x - y) for x, y in zip(d1, d2))



prod = product
MIN = -10**100
MAX = 10**100
