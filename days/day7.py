from collections import defaultdict


def count_splits(lines):
    """
    Count the splits,timelines for a tachyon map
    """
    cur = defaultdict(int)
    splits = 0
    for l in lines:
        for i, c in enumerate(l):
            if c == "S":
                cur[i] = 1
            elif c == "^" and i in cur:
                splits += 1
                cnt = cur.pop(i)
                if i > 0:
                    cur[i - 1] += cnt
                if i < (len(l.strip()) - 1):
                    cur[i + 1] += cnt
    return splits, sum(cur.values())


def run(fs):
    return count_splits(fs)
