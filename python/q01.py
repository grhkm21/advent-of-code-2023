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
    s = 0
    for line in data:
        nums = re.findall(r"\d", line)
        try:
            s += int(nums[0] + nums[-1])
        except:
            print("error:", line)
    return s


def part2(data):
    nums = [
        "zero", "one", "two", "three", "four", "five", "six", "seven", "eight",
        "nine"
    ]
    for d in range(10):
        nums.append(str(d))
    tot = 0
    for line in data:
        cur = []
        for i in range(len(line)):
            for d in nums:
                if line[i:].startswith(d):
                    cur.append(str(nums.index(d) % 10))
        tot += int(cur[0] + cur[-1])
    return tot


if __name__ == "__main__":
    data = parse_data()
    print("[!] part1:", part1(data))
    print("[!] part2:", part2(data))
