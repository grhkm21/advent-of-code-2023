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
        lines = fin.read().strip().split("\n")

    return lines


def solve(data):
    part1 = 0
    part2 = 0

    for line in data:
        pass

    return (part1, part2)


if __name__ == "__main__":
    data = parse_data()
    part1, part2 = solve(data)
    print("[!] part1:", part1)
    print("[!] part2:", part2)
