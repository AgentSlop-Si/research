"""Minimal exact API example; the known formula is not a lower-bound input."""
from fractions import Fraction
from pathlib import Path
import json
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent))
from adapter import Field, CountingOracle, complete

n = 5
identity, successor = list(range(n)), [(i + 1) % n for i in range(n)]
data = {"r0": identity, "r1": successor, "s0": identity, "s1": successor,
        "a": [1] * n, "b": [-2] * n, "d": [1] * n, "e": [-3] * n}

def target_entry(i, j):
    distance = (j - i) % n
    return Fraction(2 ** distance, 1 - 2 ** n) + Fraction(3 ** distance, 1 - 3 ** n)

oracle = CountingOracle(target_entry)
answer = complete(data, oracle, Field())
print(json.dumps({"ok": answer["ok"], "n": n, "target_queries": oracle.calls,
                  "x": [str(x) for x in answer["x"]], "y": [str(y) for y in answer["y"]],
                  "target_invertibility_checked": answer["target_invertibility_checked"]}, indent=2))
