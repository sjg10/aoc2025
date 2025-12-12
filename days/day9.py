from collections import defaultdict
from heapq import heappop, heappush


class DescOrderNodePairs:
    """
    Store a pair of nodes with area, in reverse order by area for heapq
    """

    def __init__(self, area, n1, n2):
        self.area = area
        self.n1 = n1
        self.n2 = n2

    def __lt__(self, o):
        return self.area > o.area  # reverse order

    def __repr__(self):
        return str(self.entity)

    def get(self):
        return self.area, self.n1, self.n2


class RectFinder:
    def __init__(self, lines):
        self.maxarea = 0
        nodes = []
        self.pairs = []
        self.up_edges = defaultdict(set)
        self.down_edges = defaultdict(set)
        self.left_edges = defaultdict(set)
        self.right_edges = defaultdict(set)
        for l in lines:
            nn = tuple(map(int, l.strip().split(",")))
            if len(nodes) > 0:
                self._add_edge(nodes[-1], nn)
            nodes.append(nn)
            for n in nodes:
                area = RectFinder._area(n, nn)
                heappush(self.pairs, DescOrderNodePairs(area, n, nn))
                if area > self.maxarea:
                    self.maxarea = area
        self._add_edge(nodes[-1], nodes[0])

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
        while True:
            area, p1, p2 = heappop(self.pairs).get()
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
            return area


def run(fs):
    rf = RectFinder(fs)
    return rf.p1(), rf.p2()
