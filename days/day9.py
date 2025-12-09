from itertools import combinations
from collections import defaultdict


class RectFinder:
    def __init__(self, lines):
        self.maxarea = 0
        self.nodes = []
        self.up_edges = defaultdict(set)
        self.down_edges = defaultdict(set)
        self.left_edges = defaultdict(set)
        self.right_edges = defaultdict(set)
        for l in lines:
            nn = tuple(map(int, l.strip().split(",")))
            if len(self.nodes) > 0:
                self._add_edge(self.nodes[-1], nn)
            self.nodes.append(nn)
            for n in self.nodes:
                area = RectFinder._area(n, nn)
                if area > self.maxarea:
                    self.maxarea = area
        self._add_edge(self.nodes[-1], self.nodes[0])

    def _add_edge(self, a, b):
        """
        Encode a->b as an set of edge pieces, merged in to an easy lookup dict
        """
        if a != b:
            if a[0] == b[0]:
                if a[1] < b[1]:
                    for x in range(a[1], b[1]):
                        self.down_edges[x].add(a[0])
                else:
                    for x in range(b[1] + 1, a[1] + 1):
                        self.up_edges[x].add(a[0])
            else:
                if a[0] < b[0]:
                    for x in range(a[0], b[0]):
                        self.right_edges[x].add(a[1])
                    self.right_edges[a[1]].update(range(a[0], b[0]))
                else:
                    for x in range(b[0] + 1, a[0] + 1):
                        self.left_edges[x].add(a[1])

    def _area(a, b):
        return (abs(a[0] - b[0]) + 1) * (abs(a[1] - b[1]) + 1)

    def p1(self):
        return self.maxarea

    def p2(self):
        maxarea = 0
        for a, b in combinations(range(len(self.nodes)), 2):
            p1 = self.nodes[a]
            p2 = self.nodes[b]
            area = RectFinder._area(p1, p2)
            if area > maxarea:
                # Arrange the points in order
                if p1[0] == p2[0] or p1[1] == p2[1]:
                    continue  # ignore straight lines
                if p1[1] > p2[1]:  # ensure p1 is above p2
                    p1, p2 = p2, p1
                if p1[0] < p2[0]:
                    topleft = p1
                    bottomright = p2
                    topright = (p2[0], p1[1])
                    bottomleft = (p1[0], p2[1])
                else:
                    topleft = (p2[0], p1[1])
                    bottomright = (p1[0], p2[1])
                    bottomleft = p2
                    topright = p1
                # Then check the edges of the rectangle, to see if the polygon "cuts in" there
                if not set(range(topleft[0], topright[0])).isdisjoint(
                    self.down_edges[topleft[1]]
                ):
                    continue
                if not set(range(topright[1], bottomright[1])).isdisjoint(
                    self.left_edges[topright[0]]
                ):
                    continue
                if not set(range(bottomright[0], bottomleft[0], -1)).isdisjoint(
                    self.up_edges[bottomright[1]]
                ):
                    continue
                if not set(range(bottomleft[1], topleft[1], -1)).isdisjoint(
                    self.right_edges[bottomleft[0]]
                ):
                    continue
                maxarea = area
        return maxarea


def run(fs):
    rf = RectFinder(fs)
    return rf.p1(), rf.p2()
