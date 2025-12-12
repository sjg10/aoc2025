from queue import LifoQueue, Empty


class Polynimo:
    """
    Store a polynimo present, and all its rotations/mirrors as bitmasks
    """

    def __init__(self, three_lines):
        self.grid = [list(line.strip()) for line in three_lines]
        grid = self.grid
        self.opts = set()
        for _ in range(4):
            self._add_opt(grid)
            grid = self._rotate(grid)
        grid = self._mirror(grid)
        for _ in range(4):
            self._add_opt(grid)
            grid = self._rotate(grid)

    def area(self):
        """
        Get the area covered by the polynimo
        """
        return sum(row.count("#") for row in self.grid)

    def set_tree_width(self, w):
        """
        Set tree width w so we reshift bitmasks for a given tree
        """
        self.wopts = []
        for opt in self.opts:
            newopt = 0
            for i, l in enumerate(opt):
                newopt |= l << (i * w)
            self.wopts.append(newopt)

    def _rotate(self, grid):
        return list(map("".join, zip(*reversed(grid))))

    def _mirror(self, grid):
        return [list(reversed(l)) for l in grid]

    def _add_opt(self, grid):
        opt = [0, 0, 0]
        for i, l in enumerate(grid):
            x = 0
            for j, c in enumerate(l):
                if c == "#":
                    x |= 2**j
            opt[i] = x
        self.opts.add(tuple(opt))

    def get_variant(self, i):
        """
        Get the i-th bitmask variant, after setting tree width
        """
        return self.wopts[i]

    def get_variant_cnt(self):
        """
        Get the number of distinct variants.
        """
        return len(self.wopts)


class Tree:
    """
    Store a tree ad pack in its presents
    """

    def __init__(self, line: str, presents: list[Polynimo]):
        size, cnts = line.split(": ")
        self.size = tuple(map(int, size.split("x")))
        self.cnts = list(map(int, cnts.split(" ")))
        self.cur = 0
        self.presents = presents

    def pack(self):
        if self._area_check() is False:
            return False
        for p in self.presents:
            p.set_tree_width(self.size[0])
        return self._pack()

    def _area_check(self):
        area = self.size[0] * self.size[1]
        required = sum(
            self.presents[i].area() * self.cnts[i] for i in range(len(self.cnts))
        )
        return area >= required

    def _add_present(self, cur, i, r, c, v):
        x = self.presents[i].get_variant(v) << ((r * self.size[0]) + c)
        return cur | x if cur & x == 0 else None

    def _remove_present(self, cur, i, r, c, v):
        y = self.presents[i].get_variant(v) << ((r * self.size[0]) + c)
        return cur ^ y

    def _attempt_pack(self, cur, i, start_r, start_c, start_v):
        newcur = None
        r = start_r
        c = start_c
        v = start_v
        while newcur is None:
            if (
                v < self.presents[i].get_variant_cnt()
            ):  # in case asked to start too late
                newcur = self._add_present(cur, i, r, c, v)
                if newcur is not None:
                    return newcur, r, c, v  # new pack
                v += 1
            if v >= self.presents[i].get_variant_cnt():
                v = 0
                c += 1
            if c > self.size[0] - 3:
                v = 0
                c = 0
                r += 1
            if r > self.size[1] - 3:
                return None  # no way to pack
        assert False  # shouldnt reach here, as no break in loop, only returns

    def _pack(self):
        packed = [0 for _ in range(len(self.cnts))]
        cur = 0
        bt = LifoQueue()
        i, r, c, v = 0, 0, 0, 0
        while i < len(packed):
            while packed[i] < self.cnts[i]:
                res = self._attempt_pack(cur, i, r, c, v)
                if res is None:
                    try:
                        i, r, c, v = bt.get(block=False)
                    except Empty:
                        return False  # no more backtrace, failed
                    cur = self._remove_present(cur, i, r, c, v)
                    packed[i] -= 1
                    v += 1
                else:
                    # present could go here, so no problem, add action to backtrace, and present in cur
                    cur, r, c, v = res
                    packed[i] += 1
                    bt.put((i, r, c, v))
                    r, c, v = 0, 0, 0
                pass
            i += 1  # all presents of this type packed, continue
        # all are packed:
        return True


class PresentPack:
    """
    Store all presents and trees
    """
    def __init__(self, lines):
        self.presents = []
        self.trees = []
        self.cur_present = []
        for l in lines:
            if ":" in l:
                if "x" in l:
                    self.trees.append(Tree(l, self.presents))
                else:
                    assert l.split(":")[0] == str(len(self.presents))
            elif l.strip() == "":
                if self.cur_present:
                    self.presents.append(Polynimo(self.cur_present))
                    self.cur_present = []
            else:
                self.cur_present.append(l.strip())

    def p1(self):
        return sum(1 if t.pack() else 0 for t in self.trees)


def run(fs):
    pp = PresentPack(fs)
    return pp.p1(), "Merry Christmas!"
