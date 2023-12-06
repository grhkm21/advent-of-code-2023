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


prod = product
MIN = -10**100
MAX = 10**100
