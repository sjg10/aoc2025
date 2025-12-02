import itertools


def find_ids(lines):
    """
    Find the invalid ids for both counting strategies
    """
    inv_sum = 0
    inv_sum_2 = 0
    for l in lines:
        for rng in l.split(","):
            if len(rng) == 0:
                continue
            lows, highs = rng.split("-")
            high = int(highs)
            low = int(lows)
            found = set()
            for rpt in itertools.count(2):
                seed = 10 ** ((len(lows) + 1) // rpt - 1)
                if seed < 1:
                    break
                while True:
                    val = int(str(seed) * rpt)
                    if val > high:
                        break
                    elif val >= low and val not in found:
                        found.add(val)
                        if rpt == 2:
                            inv_sum += val
                        inv_sum_2 += val
                    seed += 1
    return inv_sum, inv_sum_2


def run(fs):
    return find_ids(fs)
