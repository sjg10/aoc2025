import heapq
import numpy as np
from sympy import Eq, solve, abc, IndexedBase
from sympy.tensor import get_indices
from itertools import count, product
from math import gcd


class Machine:
    def __init__(self, line):
        ls = line.split()
        self.aim = 0
        for i, c in enumerate(ls[0][1:-1]):
            if c == "#":
                self.aim += 2**i
        self.light_cnt = len(ls[0]) - 2
        self.size = 2 ** (self.light_cnt)
        self.buttons = []
        for buttonset in ls[1:-1]:
            cur = 0
            for b in buttonset[1:-1].split(","):
                cur |= pow(2, int(b))
            self.buttons.append(cur)
        self.end = set(ls[-1].split(","))

    def lightup(self):
        # print("\nAim", rep(self.aim, self.light_cnt))
        visited = {0: 0}
        h = [(0, 0)]
        nodes = set(range(self.size))
        while nodes and h:
            current_weight, min_node = heapq.heappop(h)
            try:
                while min_node not in nodes:
                    current_weight, min_node = heapq.heappop(h)
            except IndexError:
                break
            # print("Visiting", rep(min_node, self.light_cnt))
            if min_node == self.aim:
                # print("Arrived", current_weight)
                return current_weight

            nodes.remove(min_node)

            for bs in self.buttons:
                v = min_node ^ bs
                # print("To", rep(v, self.light_cnt))
                weight = current_weight + 1
                if v not in visited or weight < visited[v]:
                    visited[v] = weight
                    heapq.heappush(h, (weight, v))
        return None

    def jolt(self):
        # print("\nAim", rep(self.aim, self.light_cnt))
        visited = {0: 0}
        h = [(0, 0)]
        nodes = set(range(self.size))
        while nodes and h:
            current_weight, min_node = heapq.heappop(h)
            try:
                while min_node not in nodes:
                    current_weight, min_node = heapq.heappop(h)
            except IndexError:
                break
            # print("Visiting", rep(min_node, self.light_cnt))
            if min_node == self.aim:
                # print("Arrived", current_weight)
                return current_weight

            nodes.remove(min_node)

            for bs in self.buttons:
                v = min_node ^ bs
                # print("To", rep(v, self.light_cnt))
                weight = current_weight + 1
                if v not in visited or weight < visited[v]:
                    visited[v] = weight
                    heapq.heappush(h, (weight, v))
        return None


class Factory:
    def __init__(self, lines):
        self.machines = [Machine(l.strip()) for l in lines]

    def p1(self):
        return sum(m.lightup() for m in self.machines)

    def p2(self):
        return sum(m.jolt() for m in self.machines)


def run(fs):
    f = Factory(fs)
    return f.p1(), f.p2()
