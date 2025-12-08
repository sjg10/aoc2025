import heapq
from dataclasses import dataclass
from math import prod, sqrt


@dataclass(frozen=True)
class Node:
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"


class Pair(object):
    def __init__(self, a: Node, b: Node, aidx: int, bidx: int):
        self.val = abs(a.x - b.x) ** 2 + abs(a.y - b.y) ** 2 + abs(a.z - b.z) ** 2
        self.pair = (aidx, bidx)

    def __lt__(self, other):
        return self.val < other.val

    def __repr__(self):
        return f"({self.pair[0]}:{self.pair[1]}={self.val})"

    def get_pair(self):
        return self.pair


class Circuits:
    def __init__(self, lines):
        self.pairs = []  # heap of all pairs, ordered by proximity
        self.nodes = []
        for l in lines:
            node = Node(*map(int, l.strip().split(",")))
            curidx = len(self.nodes)
            for i, n in enumerate(self.nodes):
                heapq.heappush(self.pairs, Pair(node, n, curidx, i))
            self.nodes.append(node)

    def join(self, initpaircnt):
        circuits = {}
        circuit_sizes = {}
        nxt_circuit_idx = 0
        pairnct = len(self.pairs)
        total_nodes = len(self.nodes)
        p1 = None
        p2 = None
        for i in range(pairnct):
            if i == initpaircnt:
                # Now find the largest circuits
                p1 = prod(sorted(circuit_sizes.values())[-3:])
            p = heapq.heappop(self.pairs).get_pair()
            mapped_0 = p[0] in circuits
            mapped_1 = p[1] in circuits
            if mapped_0 and not mapped_1:  # place 1 in 0's circuit
                circuits[p[1]] = circuits[p[0]]
                circuit_sizes[circuits[p[0]]] += 1
            elif mapped_1 and not mapped_0:  # place 0 in 1's circuit
                circuits[p[0]] = circuits[p[1]]
                circuit_sizes[circuits[p[1]]] += 1
            elif mapped_0 and mapped_1:  # already both in a circuit
                if circuits[p[0]] == circuits[p[1]]:
                    continue  # ignore in same circuit already
                keeping = circuits[p[0]]
                dropping = circuits[p[1]]
                dropcnt = circuit_sizes.pop(dropping)
                circuit_sizes[keeping] += dropcnt
                for x in circuits:
                    if circuits[x] == dropping:
                        circuits[x] = keeping
            else:  # new circuit
                circuits[p[0]] = nxt_circuit_idx
                circuits[p[1]] = nxt_circuit_idx
                circuit_sizes[nxt_circuit_idx] = 2
                nxt_circuit_idx += 1
            if len(circuit_sizes) == 1 and circuit_sizes[circuits[p[1]]] == total_nodes:
                p2 = self.nodes[p[0]].x * self.nodes[p[1]].x
            if p1 is not None and p2 is not None:
                break
        return p1, p2


def run(fs):
    cs = Circuits(fs)
    return cs.join(1000)
