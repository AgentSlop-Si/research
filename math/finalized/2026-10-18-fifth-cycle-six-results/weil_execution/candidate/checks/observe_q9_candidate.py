"""New observation adapter; contains no oracle or passing verdict."""
import json
import sys

sys.path.insert(0, "/tmp/weil-work")
import local_ring_weil as candidate

q, p, k = 9, 3, 2
ell, zeta = candidate.coefficient_field(q)
rows = []
for b in range(-q, 2 * q):
    rows.append({
        "b": b,
        "fourier": candidate.upper_shear_matrix(q, b, ell, zeta),
        "gauss": candidate.upper_shear_gauss_matrix(q, b, ell, zeta),
        "completed": candidate.predicted_upper_shear(q, p, k, b, ell, zeta),
    })
print(json.dumps({"q": q, "p": p, "k": k, "modulus": ell, "root": zeta, "rows": rows}, sort_keys=True))
