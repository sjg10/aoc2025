from collections import defaultdict


class PaperMap:
    """
    Store a map of rolls of paper
    """

    def __init__(self, lines):
        self.paper = []
        self.nbors = defaultdict(int)
        for r, l in enumerate(lines):
            for c, p in enumerate(l):
                if p == "@":
                    self.paper.append((r, c))
                    # add to all nbors, even outside map, as they wont be paper so will be ignored
                    self._add_nbors(r, c, 1)

    def _add_nbors(self, r, c, n):
        """
        Add n to all nbors of r,c
        """
        for x in [-1, 0, 1]:
            for y in [-1, 0, 1]:
                if x == y == 0:
                    continue
                self.nbors[(r + x, c + y)] += n

    def get_4_nbors(self):
        """
        Get paper with 4 nbors
        """
        return len([x for x in self.paper if self.nbors[x] < 4])

    def get_total_removed(self):
        """
        Get total count of nbors we can remove. Destructive.
        """
        total_removed = 0
        while True:
            removed = 0
            for x in filter(lambda x: self.nbors[x] < 4, self.paper):
                removed += 1
                self._add_nbors(x[0], x[1], -1)
                self.nbors[x] = (
                    100000000  # to delete the paper without modifying self.paper in place
                )
            if removed == 0:
                break
            total_removed += removed
        return total_removed


def run(fs):
    pm = PaperMap(fs)
    return pm.get_4_nbors(), pm.get_total_removed()
