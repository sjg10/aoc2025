class CafeteriaInventory:
    def __init__(self, lines):
        rangeparse = True
        self.ranges = []
        self.inventory = []
        for l in lines:
            if len(l.strip()) == 0:
                rangeparse = False
            elif rangeparse:
                r = l.split("-")
                self._new_range(int(r[0]), int(r[1]))
            else:
                self.inventory.append(int(l))

    def _new_range(self, s, e):
        remove_ranges = []
        for i, r in enumerate(self.ranges):
            if s >= r[0] and e <= r[1]:
                return  # the range is fully contained in another, so we dont care
            elif s <= r[0] and e >= r[1]:
                # New range fully contains previous range, remove it.
                remove_ranges.append(i)
            elif s <= r[0] and e <= r[1] and e >= r[0]:  # left overlap
                self.ranges[i][0] = e + 1
            elif s >= r[0] and s <= r[1] and e >= r[1]:  # right extends
                self.ranges[i][1] = s - 1
        for index in sorted(remove_ranges, reverse=True):
            del self.ranges[index]
        self.ranges.append([s, e])

    def get_fresh(self):
        fresh = 0
        for i in self.inventory:
            for r in self.ranges:
                if i >= r[0] and i <= r[1]:
                    fresh += 1
                    break
        return fresh

    def get_fresh_possible(self):
        s = 0
        for r in self.ranges:
            s += 1 + r[1] - r[0]
        return s


def run(fs):
    ci = CafeteriaInventory(fs)
    return ci.get_fresh(), ci.get_fresh_possible()
