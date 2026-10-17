#!/usr/bin/env python3
"""Check full shifted-resultant data by a multiplication-matrix determinant.

This is a separate reviewer implementation. It imports only the reviewer's
integer Gaussian recurrence and SymPy. It does not execute producer code.
"""
import hashlib
import json
from math import comb
from pathlib import Path
import sympy
from sympy import GF, symbols
from sympy.polys.matrices import DomainMatrix
from verify_data_only import gaussian_rows

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "sources/reduction_orders.json"
t = symbols("t")


def main():
    raw = SOURCE.read_bytes()
    data = json.loads(raw)
    expected = {(3,b) for b in range(3,9)} | {(5,b) for b in range(5,11)} | {(7,b) for b in [7,8]}
    assert len(data) == len(expected) == 14
    assert {(r["prime"],r["b"]) for r in data} == expected
    rows = gaussian_rows(10)
    checks = []
    for r in data:
        p,b = r["prime"], r["b"]
        ring = GF(p).poly_ring(t)
        H = []
        for a in rows[b]:
            shifted = [sum(a[j]*comb(j,i) for j in range(i,len(a))) % p for i in range(len(a))]
            H.append(ring.from_sympy(sum(c*t**i for i,c in enumerate(shifted))))
        assert H[-1] == ring.one
        # In the monic quotient R[z]/(H), det(multiplication by H') is Res(H,H').
        v = [ring(i+1)*H[i+1] for i in range(b)]
        columns = []
        for j in range(b):
            columns.append(v[:])
            leading = v[-1]
            v = [ring.zero]+v[:-1]
            v = [v[i]-leading*H[i] for i in range(b)]
        M = [[columns[j][i] for j in range(b)] for i in range(b)]
        resultant = DomainMatrix.from_list(M,ring).det()
        sparse = {str(exp[0]): int(c)%p for exp,c in resultant.to_dict().items() if c}
        assert sparse == r["resultant_shifted_sparse"], (p,b,"full coefficient mismatch")
        assert sparse, (p,b,"identically zero reduction")
        order = min(int(k) for k in sparse)
        e = b*(b-1)//2
        assert order >= e
        assert order == r["disc_order_mod_p_at_1"]
        assert order-e == r["V_order_mod_p_at_1"]
        sign = (-1)**e
        disc = {k:(sign*c)%p for k,c in sparse.items()}
        deflated = {str(int(k)-e): c for k,c in disc.items()}
        check = {"prime": p, "b": b,
                 "method": "determinant of multiplication by ordinary H_z in GF(p)[t,z]/H(z;1+t)",
                 "full_shifted_resultant_coefficients_match": True,
                 "nonzero_reduction": True,
                 "D_to_resultant_sign": sign,
                 "universal_deflation_exponent": e,
                 "D_order_at_q1_mod_p": order,
                 "V_order_at_q1_mod_p": order-e,
                 "V_leading_coefficient_mod_p": deflated[str(order-e)],
                 "V_mod_p_shifted_sparse": deflated}
        checks.append(check)
        print(f"PASS p={p}, b={b}: full resultant coefficients, ord(D)={order}, e={e}, ord(V)={order-e}",flush=True)
    result = {"decision":"PASS", "source_sha256":hashlib.sha256(raw).hexdigest(),
              "sympy_version":sympy.__version__, "records_checked":len(checks),
              "scope":"Ordinary residual discriminant obstruction only; no node separation", "records":checks}
    (BASE/"reduction_order_verification.json").write_text(json.dumps(result,indent=2)+"\n")


if __name__ == "__main__":
    main()
