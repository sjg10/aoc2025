class DeviceGraph:
    def __init__(self, lines):
        self.adj = {}
        for l in lines:
            src, targets = l.strip().split(": ")
            self.adj[src] = targets.split(" ")

    def p1(self):
        return self._path_count("you", "out")

    def p2(self):
        s2f = self._path_count("svr", "fft", excl="dac")
        s2d = self._path_count("svr", "dac", excl="fft")
        f2d = self._path_count("fft", "dac", excl="out")
        d2f = self._path_count("dac", "fft", excl="out")
        d2o = self._path_count("dac", "out", excl="fft")
        f2o = self._path_count("fft", "out", excl="dac")
        return (s2f * f2d * d2o) + (s2d * d2f * f2o)

    def _path_count(self, start, end, excl=None):
        return self._dfs(start, end, {}, excl)

    def _dfs(self, u, dest, memo, excl=None):
        if u == dest:
            return 1

        if u in memo:
            return memo[u]

        count = 0
        for v in self.adj.get(u, []):
            if v != excl:
                count += self._dfs(v, dest, memo, excl)

        memo[u] = count
        return count


def run(fs):
    dg = DeviceGraph(fs)
    return dg.p1(), dg.p2()
