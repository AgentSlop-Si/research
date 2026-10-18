"""Fresh independent finite offline oracle. Does not import the online policy.

At each service instant enumerate every legal cache containing the requested
view. Between service instants arbitrary paid prefetching and free disposal are
allowed. Transition C -> D costs sum(F[v] for v in D-C). This is both achievable
(evict C-D, then load D-C) and unavoidable. Empty start is charged.
"""
from fractions import Fraction
from itertools import combinations
from heapq import heappush, heappop


class OfflineOracle:
    def __init__(self, capacity, tariffs):
        self.k = capacity
        self.tariffs = {v: Fraction(f) for v, f in tariffs.items()}
        self.universe = tuple(sorted(tariffs))
        self.states = tuple(frozenset(s) for n in range(min(capacity, len(tariffs)) + 1)
                            for s in combinations(self.universe, n))
        self.empty = self.states.index(frozenset())
        self.target = {v: tuple(i for i, s in enumerate(self.states) if v in s)
                       for v in self.universe}
        self.cost = tuple(tuple(sum((self.tariffs[v] for v in d - c), Fraction(0))
                                for d in self.states) for c in self.states)

    def initial(self):
        return {self.empty: Fraction(0)}

    def step(self, previous, request, available=None):
        result = {}
        for d in self.target[request]:
            if available is not None and not self.states[d] <= available:
                continue
            result[d] = min(c + self.cost[s][d] for s, c in previous.items())
        return result

    def solve(self, sequence, availability=None):
        dp = self.initial()
        for t, v in enumerate(sequence):
            dp = self.step(dp, v, None if availability is None else availability[t])
        return min(dp.values())


def action_graph_optimum(sequence, capacity, tariffs):
    """Second oracle: shortest-path closure via individual load/evict actions.

    It intentionally does not use OfflineOracle's state/transition formulas.
    """
    tariffs = {v: Fraction(f) for v, f in tariffs.items()}
    dist = {frozenset(): Fraction(0)}
    serial = 0
    for request in sequence:
        heap = []
        for state, value in dist.items():
            heappush(heap, (value, serial, state))
            serial += 1
        while heap:
            value, _, state = heappop(heap)
            if dist[state] != value:
                continue
            successors = [(state - {v}, Fraction(0)) for v in state]
            if len(state) < capacity:
                successors += [(state | {v}, f) for v, f in tariffs.items() if v not in state]
            for target, charge in successors:
                new = value + charge
                if target not in dist or new < dist[target]:
                    dist[target] = new
                    heappush(heap, (new, serial, target))
                    serial += 1
        dist = {s: c for s, c in dist.items() if request in s}
    return min(dist.values())
