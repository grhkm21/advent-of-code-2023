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

prod = product
