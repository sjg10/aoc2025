import operator


def find_batteries(lines, ons=2):
    """
    Find the battery choice for a given number of battery turn ons, and sum
    """
    sm = 0
    for l in lines:
        l = l.strip()
        res = 0
        maxidx = -1
        for rem in range(ons - 1, -1, -1):
            if rem > 0:
                maxidx, maxv = max(
                    enumerate(l[maxidx + 1 : -rem], start=maxidx + 1),
                    key=operator.itemgetter(1),
                )
            else:
                maxidx, maxv = max(
                    enumerate(l[maxidx + 1 :], start=maxidx + 1),
                    key=operator.itemgetter(1),
                )
            res = res * 10 + int(maxv)
        sm += res
    return sm


def run(fs):
    p1 = find_batteries(fs, 2)
    fs.seek(0)
    p2 = find_batteries(fs, 12)
    return p1, p2
