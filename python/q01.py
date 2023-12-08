import os
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
import timeit
import regex

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


def main(file=sys.stdout):
    data = parse_data()
    print("[!] part1:", part1(data), file=file)
    print("[!] part2:", part2(data), file=file)


if __name__ == "__main__":
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

