from math import prod
from operator import itemgetter
import re
from collections import defaultdict
from enum import Enum


def p1(cs, os):
    total = 0
    for i, o in enumerate(os):
        if o == "+":
            total += sum(map(int, cs[i]))
        else:
            total += prod(map(int, cs[i]))
    return total


def p2(cs, os, alignments):
    total = 0
    for i, col in enumerate(cs):
        colwidth = max(len(x) for x in col)
        # Re-add spaces
        if len(set(alignments[i])) == 1:  # leftaligned
            for j in range(len(col)):
                col[j] = col[j] + (" " * (colwidth - len(col[j])))
        else:  # right aligned
            for j in range(len(col)):
                col[j] = (" " * (colwidth - len(col[j]))) + col[j]
        # Transpose
        col = [int("".join(x)) for x in zip(*col)]
        if os[i] == "+":
            total += sum(col)
        else:
            total += prod(col)
    return total


def do_homework(lines):
    cs = None
    alignments = None
    for l in lines:
        if l[0] in ["+", "*"]:
            s = l.split()
            return p1(cs, s), p2(cs, s, alignments)
        s = [(m.start(), m.group(1)) for m in re.finditer(r"(\d+)", l)]
        if cs is None:
            cs = [[] for i in range(len(s))]
            alignments = [[] for i in range(len(s))]
        for i, x in enumerate(s):
            cs[i].append(x[1])
            alignments[i].append(x[0])


def run(fs):
    return do_homework(fs)
