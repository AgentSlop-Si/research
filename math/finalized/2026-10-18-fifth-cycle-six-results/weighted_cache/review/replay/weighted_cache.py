"""Fresh deterministic equal-slot weighted caching implementation, 2026-10-18.

Self-authored for ALG-070. Standard library only. Credits are exact Fractions.
This module has no persistence, network, input-code loading, or side effects.
"""
from fractions import Fraction


class WeightedCache:
    def __init__(self, capacity, tariffs):
        if not isinstance(capacity, int) or capacity < 1:
            raise ValueError("capacity must be a positive integer")
        self.capacity = capacity
        if set(tariffs) != set(range(len(tariffs))):
            raise ValueError("registry handles must be consecutive nonnegative integers")
        self.tariffs = [Fraction(tariffs[v]) for v in range(len(tariffs))]
        if any(f <= 0 for f in self.tariffs):
            raise ValueError("tariffs must be positive")
        self.credit = {}
        self.total = Fraction(0)
        self.build_count = 0

    def register_tariff(self, view, tariff):
        """Paid registry extension; existing handles cannot be repriced."""
        tariff = Fraction(tariff)
        if tariff <= 0:
            raise ValueError("tariffs must be positive")
        if view == len(self.tariffs):
            self.tariffs.append(tariff)
        elif 0 <= view < len(self.tariffs) and self.tariffs[view] == tariff:
            return
        else:
            raise ValueError("registration must preserve immutable tariffs and dense handles")

    def request(self, view):
        """Return True iff a paid complete materialization is required.

        Integer handles are ordered for deterministic zero-credit tie breaking.
        The caller must actually build the complete view when this returns True.
        """
        f = self.tariffs[view]
        if view in self.credit:
            self.credit[view] = f
            return False
        if len(self.credit) == self.capacity:
            delta = min(self.credit.values())
            for v in self.credit:
                self.credit[v] -= delta
            victim = min(v for v, c in self.credit.items() if c == 0)
            del self.credit[victim]
        self.credit[view] = f
        self.total += f
        self.build_count += 1
        assert len(self.credit) <= self.capacity
        assert all(0 <= c <= self.tariffs[v] for v, c in self.credit.items())
        return True


def run(sequence, capacity, tariffs):
    policy = WeightedCache(capacity, tariffs)
    for view in sequence:
        policy.request(view)
    return policy
