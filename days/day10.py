import heapq
import pulp


class Machine:
    def __init__(self, line):
        ls = line.split()
        self.aim = tuple(c == "#" for c in ls[0][1:-1])
        self.buttons = []
        for buttonset in ls[1:-1]:
            self.buttons.append(set(map(int, buttonset[1:-1].split(","))))
        self.counter_aim = tuple(map(int, ls[-1][1:-1].split(",")))

    def lightup(self):
        initial = tuple(False for _ in self.aim)
        visited = {initial: 0}
        h = [(0, initial)]
        while h:
            current_weight, min_node = heapq.heappop(h)
            if min_node == self.aim:
                return current_weight

            for bs in self.buttons:
                v = list(min_node)
                for b in bs:
                    v[b] = not v[b]
                v = tuple(v)
                weight = current_weight + 1
                if v not in visited or weight < visited[v]:
                    visited[v] = weight
                    heapq.heappush(h, (weight, v))
        return None

    def jolt(self):
        prob = pulp.LpProblem("MachineJolt", pulp.LpMinimize)
        self.btnvars = []

        for i in range(len(self.buttons)):
            self.btnvars.append(pulp.LpVariable(f"btn{i}", 0, None, pulp.LpInteger))
        # objective
        prob += pulp.lpSum(self.btnvars), "TotalButtonPresses"
        # constraints
        for i in range(len(self.counter_aim)):
            prob += (
                pulp.lpSum(
                    self.btnvars[j]
                    for j in range(len(self.buttons))
                    if (i in self.buttons[j])
                )
                == self.counter_aim[i],
                f"Counter{i}",
            )
        prob.solve(pulp.PULP_CBC_CMD(msg=0))
        return int(pulp.value(prob.objective))


class Factory:
    def __init__(self, lines):
        self.machines = [Machine(l.strip()) for l in lines]

    def p1(self):
        return sum(m.lightup() for m in self.machines)

    def p2(self):
        return sum(m.jolt() for m in self.machines)


def run(fs):
    f = Factory(fs)
    return f.p1(), f.p2()
