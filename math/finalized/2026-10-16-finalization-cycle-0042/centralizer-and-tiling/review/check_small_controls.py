"""Independent exact controls; no source programs or network accesses."""
import itertools
import json
import math
from pathlib import Path

out = {"monomial": [], "rectangles": []}
for n in range(2, 7):
    checked = accepted = 0
    for tau in itertools.permutations(range(n)):
        inv = [tau.index(i) for i in range(n)]
        b = tau[0]
        exponents = [(b * tau[j]) % n for j in range(n)]
        commute = exponents[0] == 0 and all(
            (exponents[j] + i * tau[j] - exponents[inv[i]] - inv[i] * j) % n == 0
            for i in range(n) for j in range(n)
        )
        u = (tau[1] - b) % n
        predicted = (math.gcd(u, n) == 1 and (u*u-1) % n == 0
                     and 2*b % n == 0 and b*b % n == 0
                     and all(tau[j] == (u*j+b) % n for j in range(n)))
        assert commute == predicted, (n, tau)
        if predicted:
            assert all(exponents[j] == u*b*j % n for j in range(n))
            accepted += 1
        checked += 1
    out["monomial"].append({"N": n, "permutations": checked, "commuting": accepted})
for n in range(2, 7):
    subsets = [tuple(i for i in range(n) if mask >> i & 1) for mask in range(1, 1 << n)]
    divisor_minimum = min(d+n//d for d in range(1,n+1) if n%d == 0)
    tested = rank_one = 0
    for rows in subsets:
        g = math.gcd(n, *(r-rows[0] for r in rows))
        d = n//g
        for cols in subsets:
            tested += 1
            is_rank_one = all((r-rows[0])*(c-cols[0]) % n == 0 for r in rows for c in cols)
            if is_rank_one:
                a,b = len(rows),len(cols)
                assert a <= d and b <= n//d
                assert n*(a+b) >= a*b*divisor_minimum
                rank_one += 1
    out["rectangles"].append({"N":n,"rectangles":tested,"rank_one":rank_one,"predicted_optimum":n*divisor_minimum})
out["result"]="PASS"
out["boundary"]="Small exact controls supplement the written algebra; no general theorem is inferred from enumeration."
Path(__file__).with_name('INDEPENDENT_SMALL_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
